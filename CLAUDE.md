# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`amazon-paapi5` is a small Python wrapper library around Amazon's Product Advertising API 5.0, published to PyPI. All library code lives in the `amazon/` package; there are no application entry points, and there is no test suite in this repo.

## Environment & commands

Dependencies are managed with Pipenv (`Pipfile`, Python 3.9 pinned, but the package supports >=3.6 per `setup.py`).

```bash
pipenv install          # install dependencies into a virtualenv
pipenv shell             # activate the virtualenv
```

Key runtime dependency: `amightygirl-paapi5-python-sdk` (Amazon's PA-API 5.0 SDK fork) — all requests/responses are built on its types (`SearchItemsRequest`, `GetItemsRequest`, etc.).

There is no test suite, linter, or build script configured in this repo — don't assume `pytest`/`tox`/`flake8` exist. Verify any change manually against the API shapes in `amightygirl.paapi5-python-sdk` (installed into the pipenv virtualenv) since there's no local test harness to catch mismatches.

Docs are built with Sphinx from `docs/source/` into `docs/build/` (see `docs/Makefile`, `docs/requirements.txt`). The built output in `docs/build/` is checked into the repo — if you edit `docs/source/*.rst`, regenerate the build output too (`cd docs && make html`) rather than leaving them out of sync.

Packaging: `setup.py` defines the PyPI package (`amazon-paapi5`); version is duplicated in `setup.py` and `amazon/__init__.py` (`__version__`) — keep them in sync when bumping.

## Architecture

The package (`amazon/`) has four files, each with a single responsibility:

- **`paapi.py`** — the only public entry point, `AmazonAPI`. One instance holds the caller's credentials (`access_key`, `secret_key`, `partner_tag`, `country`) and wraps the SDK's `DefaultApi`. Exposes four calls: `search_items`, `search_items_pool` (same as `search_items` but builds its own `ApiClient`/`Configuration` with a configurable connection pool size, for concurrent/threaded use), `get_variations`, `get_browse_nodes`, and `get_items`.
- **`constant.py`** — per-country `REGIONS`/`DOMAINS` maps (used to build the SDK host/region), and default resource lists (`SEARCH_RESOURCES`, `ITEM_RESOURCES`, `VARIATION_RESOURCES`, `BROWSE_RESOURCES`) built from the SDK's resource enums. Each `AmazonAPI` method accepts an optional `*_resource` override to request a subset of the default resources.
- **`entities.py`** — `AmazonProduct` and `AmazonBrowseNode` wrap the SDK's raw `Item`/`BrowseNode` response objects, adding convenience properties (`bestOffer`, `isDiscount`, `isPrime`, `isFreeShipping`, `isAmazonFulfilled`, `originalPrice`) and `to_dict()`/`to_str()` for a uniform, ergonomic response shape across all four API calls.
- **`exception.py`** — `AmazonException(status, reason)`, the single exception type all four API methods normalize errors into (SDK `ApiException`, `ValueError`, `TypeError`, or a generic error are all re-raised as `AmazonException`).

### Request flow (same shape in all four `AmazonAPI` methods)

1. Build a `cache_url` from the call's parameters via `_cache_url`/`_quote_query` (deterministic, alphabetically-sorted query string).
2. If a `CacheReader` was provided to `AmazonAPI(...)` and it returns a hit for `cache_url`, return the pickled cached `{'data', 'http_info'}` without calling Amazon.
3. Otherwise build the SDK request object (e.g. `SearchItemsRequest`), sleep to respect `throttling` (time since `last_query_time`), and call the SDK (`http_info=True` uses the `*_with_http_info` SDK variant; `async_req=True` runs it on a thread and blocks on `.get()`).
4. Wrap the raw SDK response items in `AmazonProduct`/`AmazonBrowseNode`, call `CacheWriter(cache_url, ...)` if configured (pickled), and return `{'data': ..., 'http_info': ...}`.
5. Any SDK/parsing error is re-raised as `AmazonException`.

When adding a new API call or changing an existing one, follow this same pattern (cache lookup → build SDK request → throttle → call → wrap in entity → cache write → normalize errors) for consistency with the rest of the file.

`get_items`/`get_browse_nodes` return `data` as a dict keyed by ASIN/browse-node-id (via `parse_response_item`/`parse_response_browse_node`); `search_items`/`get_variations` return `data` as a plain list — this asymmetry is intentional and matches the README's documented usage.
