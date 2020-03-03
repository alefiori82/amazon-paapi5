.. Amazon paapi5 documentation master file, created by
   sphinx-quickstart on Thu Feb 27 22:28:25 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Amazon paapi5's documentation!
*****************************************

Amazon paapi5 is a thin, well-tested, maintained, and powerful Python wrapper over the Amazon Product Advertising API. There is practically no overhead, and no magic (unless you add it yourself).

Before you get started, make sure you have both Amazon Product Advertising and AWS accounts. AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_ASSOCIATE_TAG are all from your Amazon Associate Account.

Features
========

- Object oriented interface for simple usage
- Get multiple products at once
- Configurable query caching
- Compatible with Python versions 3.6 and up
- Support for AU, BR, CA, FR, IN, IT, JP, MX, ES, TR, MX, AE, UK and US Amazon Product Advertising API endpoints
- Configurable throttling for batches of queries
- Ask for new features through the `issues <https://github.com/alefiori82/amazon-paapi5/issues>`_ section.


Changelog
=========

    Version 1.1.1
        - add additional parameters to api calls
    Version 1.1.0
        - CacheReader and CacheWriter available for all the search functions
        - Defintion af AmazonException to get exceptions during the api calls
        - Constants defintion
        - AmazonProduct and AmazonBrowseNode definition
        - Uniform data structure returned by all the api calls
    Version 1.0.0
        - CacheReader and CacheWriter
        - Enable throttling
    Version 0.1.0
        - First release

Contents
========

.. toctree::
   :maxdepth: 1
   
   quickstart
   responses
   advancedUsage
   package


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. figure::  https://cdn.buymeacoffee.com/buttons/default-orange.png
   :align:   center
   :target: https://www.buymeacoffee.com/1jTO4Av





