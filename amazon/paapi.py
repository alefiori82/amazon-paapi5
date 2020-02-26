"""Amazon Product Advertising API 5.0 wrapper for Python"""

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.api_client import ApiClient
from paapi5_python_sdk.configuration import Configuration
from paapi5_python_sdk.partner_type import PartnerType


from paapi5_python_sdk.rest import ApiException


from paapi5_python_sdk.get_items_request import GetItemsRequest
from paapi5_python_sdk.search_items_request import SearchItemsRequest
from paapi5_python_sdk.get_variations_request import GetVariationsRequest
from paapi5_python_sdk.get_browse_nodes_request import GetBrowseNodesRequest



import time, json, pickle, pprint
from urllib.parse import quote as urllib_quote
from .entities import AmazonProduct, AmazonBrowseNode
from .constant import *



def _quote_query(query):
    """Turn a dictionary into a query string in a URL, with keys
    in alphabetical order."""
    return "&".join("%s=%s" % (
        k, urllib_quote(
            str(query[k]).encode('utf-8'), safe='~'))
            for k in sorted(query))

def parse_response_browse_node(browse_nodes_response_list):
    """
    The function parses Browse Nodes Response and creates a dict of BrowseNodeID to BrowseNode object
    :param browse_nodes_response_list: List of BrowseNodes in GetBrowseNodes response
    :return: Dict of BrowseNodeID to BrowseNode object
    """
    mapped_response = {}
    for browse_node in browse_nodes_response_list:
        mapped_response[browse_node.id] = browse_node
    return mapped_response


def parse_response(item_response_list):
    """
    The function parses GetItemsResponse and creates a dict of ASIN to Item object
    :param item_response_list: List of Items in GetItemsResponse
    :return: Dict of ASIN to Item object
    """
    mapped_response = {}
    for item in item_response_list:
        mapped_response[item.asin] = item
    return mapped_response


class AmazonAPI:
    """Creates an instance containing your API credentials.

    Args:
        access_key (string): Your API key.
        secret_key (string): Your API secret.
        partner_tag (string): The tag you want to use for the URL.
        country (string): Country code.
        throttling (float, optional): Reduce this value to wait longer between API calls.
    """
    def __init__(self, access_key, secret_key, partner_tag, country='US', throttling=0.9, CacheReader=None, CacheWriter=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.partner_tag = partner_tag
        self.throttling = throttling
        self.country = country
        self.host = 'webservices.amazon.' + DOMAINS[country]
        self.region = REGIONS[country]
        self.marketplace = 'www.amazon.' + DOMAINS[country]
        self.last_query_time = time.time()
        self.CacheReader = CacheReader
        self.CacheWriter = CacheWriter

        self.default_api = DefaultApi(
            access_key=self.access_key, secret_key=self.secret_key, host=self.host, region=self.region
        )
        

    def _cache_url(self, query):
        
        return self.host + "?" + _quote_query(query)



    """ Choose resources you want from SearchItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter """
    def search_items(self, keywords, brand=None, condition=None, sortBy= None, browseNode=None, search_index="All", item_count=10, http_info=False, async_req=False, search_items_resource=SEARCH_RESOURCES):
        """ Forming request """
        try:
            if item_count > 10 or item_count < 1:
                item_count = 10
            search_items_request = SearchItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                keywords=keywords,
                search_index=search_index,
                item_count=item_count,
                resources=search_items_resource,
                condition=condition,
                browse_node_id=browseNode,
                brand=brand,
                sort_by=sortBy
            )
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'keywords':keywords,
                'search_index':search_index,
                'item_count':item_count,
                'condition':condition,
                'browse_node_id': browseNode,
                'brand': brand,
                'sort_by': sortBy  }
            )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return pickle.loads(cached_response_text)
            
        except ValueError as exception:
            print("Error in forming SearchItemsRequest: ", exception)
            raise Exception(exception)

        try:
            """ Sending request """
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            if http_info:
                response_with_http_info = self.default_api.search_items_with_http_info(search_items_request)
                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    if response.search_result is not None:
                        resp = [ AmazonProduct(item) for item in response.search_result.items]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp))
                        return response_with_http_info[2], resp
                    if response.errors is not None:
                        print(
                            "\nPrinting Errors:\nPrinting First Error Object from list of Errors"
                        )
                        print("Error code", response.errors[0].code)
                        print("Error message", response.errors[0].message)
                        raise Exception(response.errors[0].message)

            else:
                if async_req:
                    thread = self.default_api.search_items(search_items_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.search_items(search_items_request)
                """ Parse response """
                if response.search_result is not None:
                    resp = [ AmazonProduct(item) for item in response.search_result.items]
                    if self.CacheWriter:
                        self.CacheWriter(cache_url, pickle.dumps(resp))
                    return resp
                if response.errors is not None:
                    print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    print("Error code", response.errors[0].code)
                    print("Error message", response.errors[0].message)
                    raise Exception(response.errors[0].message)    

        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise Exception(exception)

        except TypeError as exception:
            print("TypeError :", exception)
            raise Exception(exception)

        except ValueError as exception:
            print("ValueError :", exception)
            raise Exception(exception)

        except Exception as exception:
            print("Exception :", exception)
            raise Exception(exception)


    """ Choose resources you want from SearchItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter """
    def search_items_pool(self, keywords, brand=None, condition=None, sortBy=None, browseNode=None, search_index="All", item_count=10, search_items_resource=SEARCH_RESOURCES ,connetion_pool_max_size=12):
        """ You can specify max connection pool size here. By default it's cpu_count * 5."""
        configuration = Configuration()
        configuration.__init__(connetion_pool_max_size)

        """ API Client Declaration """
        api_client = ApiClient(
            access_key=self.access_key,
            secret_key=self.secret_key,
            host=self.host,
            region=self.region,
            configuration=configuration,
        )

        """ API declaration """
        default_api = DefaultApi(api_client=api_client)

        """ Forming request """
        try:
            if item_count > 10 or item_count < 1:
                item_count = 10
            search_items_request = SearchItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                keywords=keywords,
                search_index=search_index,
                item_count=item_count,
                resources=search_items_resource,
                condition=condition,
                browse_node_id=browseNode,
                brand=brand,
                sort_by=sortBy
            )
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'keywords':keywords,
                'search_index':search_index,
                'item_count':item_count,
                'condition':condition,
                'browse_node_id': browseNode,
                'brand': brand,
                'sort_by': sortBy }
            )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return pickle.loads(cached_response_text)

        except ValueError as exception:
            print("Error in forming SearchItemsRequest: ", exception)
            raise Exception(exception)

        try:
            """ Sending request """
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            response = default_api.search_items(search_items_request)

            """ Parse response """
            if response.search_result is not None:
                resp = [ AmazonProduct(item) for item in response.search_result.items]
                if self.CacheWriter:
                    self.CacheWriter(cache_url, pickle.dumps(resp))
                return resp
            if response.errors is not None:
                print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                print("Error code", response.errors[0].code)
                print("Error message", response.errors[0].message)
                raise Exception(response.errors[0].message)

        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise Exception(exception)

        except TypeError as exception:
            print("TypeError :", exception)
            raise Exception(exception)

        except ValueError as exception:
            print("ValueError :", exception)
            raise Exception(exception)

        except Exception as exception:
            print("Exception :", exception)
            raise Exception(exception)

    """ Choose resources you want from GetVariationsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-variations.html#resources-parameter """
    def get_variations(self, asin, condition=None, languages_of_preference=None, currency_of_preference=None, async_req=False, http_info=False, get_variations_resources=VARIATION_RESOURCES):
        """ Forming request """
        try:
            get_variations_request = GetVariationsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                languages_of_preference=languages_of_preference,
                asin=asin,
                resources=get_variations_resources,
                condition=condition,
                currency_of_preference=currency_of_preference
            )
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'asin':asin,
                'languages_of_preference':languages_of_preference,
                'condition': condition,
                'currency_of_preference': currency_of_preference
                }
                )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return pickle.loads(cached_response_text)

        except ValueError as exception:
            print("Error in forming GetVariationsRequest: ", exception)
            raise Exception(exception)

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            """ Sending request """
            if http_info:
                response_with_http_info = self.default_api.get_variations_with_http_info(get_variations_request)

                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    if response.variations_result is not None:
                        resp = [ AmazonProduct(item) for item in response.variations_result.items]
                        if self.CacheWriter:    
                            self.CacheWriter(cache_url, pickle.dumps(resp))
                        return response_with_http_info[2], resp

                    if response.errors is not None:
                        print(
                            "\nPrinting Errors:\nPrinting First Error Object from list of Errors"
                        )
                        print("Error code", response.errors[0].code)
                        print("Error message", response.errors[0].message)
                        raise Exception(response.errors[0].message)
            else:
                if async_req:
                    thread = self.default_api.get_variations(get_variations_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.get_variations(get_variations_request)

                """ Parse response """
                if response.variations_result is not None:
                    resp = [ AmazonProduct(item) for item in response.variations_result.items]
                    if self.CacheWriter:
                        self.CacheWriter(cache_url, pickle.dumps(resp))
                    return resp

                if response.errors is not None:
                    print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    print("Error code", response.errors[0].code)
                    print("Error message", response.errors[0].message)
                    raise Exception(response.errors[0].message)

        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise Exception(exception)

        except TypeError as exception:
            print("TypeError :", exception)
            raise Exception(exception)

        except ValueError as exception:
            print("ValueError :", exception)
            raise Exception(exception)

        except Exception as exception:
            print("Exception :", exception)
            raise Exception(exception)


    """ Choose resources you want from GetItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-items.html#resources-parameter """
    def get_items(self, item_ids=[], currency_of_preference=None, condition=None, http_info=False, async_req=False, get_items_resource=ITEM_RESOURCES):
        
        """ Choose item id(s) """
        if len(item_ids) == 0:
            raise Exception('No item ids specified')
        
        """ Forming request """
        try:
            get_items_request = GetItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                condition=condition,
                item_ids=item_ids,
                resources=get_items_resource,
                currency_of_preference=currency_of_preference
            )
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'item_ids':item_ids,
                'condition':condition,
                'currency_of_preference': currency_of_preference  }
                )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return parse_response(pickle.loads(cached_response_text))

        except ValueError as exception:
            print("Error in forming GetItemsRequest: ", exception)
            raise Exception(exception)

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            if http_info:
                response_with_http_info = self.default_api.get_items_with_http_info(
                    get_items_request
                )

                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    if response.items_result is not None:
                        resp = [ AmazonProduct(item) for item in response.items_result.items]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp))
                        return response_with_http_info[2], parse_response(resp)
                        
                    if response.errors is not None:
                        print(
                            "\nPrinting Errors:\nPrinting First Error Object from list of Errors"
                        )
                        print("Error code", response.errors[0].code)
                        print("Error message", response.errors[0].message)
                        raise Exception(response.errors[0].message)

            else:
                """ Sending request """
                if async_req:
                    thread = self.default_api.get_items(get_items_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.get_items(get_items_request)

                """ Parse response """
                if response.items_result is not None:
                    resp = [ AmazonProduct(item) for item in response.items_result.items]
                    if self.CacheWriter:
                        self.CacheWriter(cache_url, pickle.dumps(resp))
                    return parse_response( resp )

                if response.errors is not None:
                    print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    print("Error code", response.errors[0].code)
                    print("Error message", response.errors[0].message)
                    raise Exception(response.errors[0].message)


        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise Exception(exception)

        except TypeError as exception:
            print("TypeError :", exception)
            raise Exception(exception)

        except ValueError as exception:
            print("ValueError :", exception)
            raise Exception(exception)

        except Exception as exception:
            print("Exception :", exception)
            raise Exception(exception)



    """ Choose resources you want from GetBrowseNodesResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/getbrowsenodes.html#resources-parameter """
    def get_browse_nodes(self, browse_node_ids=[], http_info=False, async_req=False, languages_of_preference = None, get_browse_node_resources=BROWSE_RESOURCES):

        """ Specify browse_node id(s) """
        
        if isinstance(browse_node_ids, list) == False or len (browse_node_ids) == 0:
            raise Exception('Browse node ids are not in the right format')
        
        """ Forming request """
        try:
            get_browse_node_request = GetBrowseNodesRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                languages_of_preference=languages_of_preference,
                browse_node_ids=browse_node_ids,
                resources=get_browse_node_resources,
            )
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'browse_node_ids':browse_node_ids,
                'languages_of_preference':languages_of_preference }
                )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return parse_response_browse_node(pickle.loads(cached_response_text))
        except ValueError as exception:
            print("Error in forming GetBrowseNodesRequest: ", exception)
            raise Exception(exception)

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            if http_info:
                response_with_http_info = self.default_api.get_browse_nodes_with_http_info(get_browse_node_request)

                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    if response.browse_nodes_result is not None:
                        resp = [ AmazonBrowseNode(node) for node in response.browse_nodes_result.browse_nodes]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp))
                        return response_with_http_info[2], parse_response_browse_node(resp)
                        
                    if response.errors is not None:
                        print(
                            "\nPrinting Errors:\nPrinting First Error Object from list of Errors"
                        )
                        print("Error code", response.errors[0].code)
                        print("Error message", response.errors[0].message)
                        raise Exception(response.errors[0].message)

            else:
                """ Sending request """
                if async_req:
                    thread = self.default_api.get_browse_nodes(get_browse_node_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.get_browse_nodes(get_browse_node_request)

                """ Parse response """
                if response.browse_nodes_result is not None:
                    resp = [ AmazonBrowseNode(item) for item in response.browse_nodes_result.browse_nodes]
                    if self.CacheWriter:
                        self.CacheWriter(cache_url, pickle.dumps(response.browse_nodes_result.browse_nodes))
                    return parse_response_browse_node(resp)
                    
                if response.errors is not None:
                    print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    print("Error code", response.errors[0].code)
                    print("Error message", response.errors[0].message)
                    raise Exception(response.errors[0].message)

        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise Exception(exception)

        except TypeError as exception:
            print("TypeError :", exception)
            raise Exception(exception)

        except ValueError as exception:
            print("ValueError :", exception)
            raise Exception(exception)

        except Exception as exception:
            print("Exception :", exception)
            raise Exception(exception)
