Amazon Product Advertising API 5.0 wrapper for Python
=======================================================
A simple Python wrapper for the last version of the Amazon Product Advertising API. This module allows to get product information from Amazon using the official API in an easier way.
Like Bottlenose you can use cache reader and writer to limit the number of api calls.

[![Amazon API](https://img.shields.io/badge/Amazon%20API-5.0-%23FD9B15)](https://webservices.amazon.com/paapi5/documentation/)


Features
--------

* Object oriented interface for simple usage.
* Get multiple products at once.
* Use cache to save api calls
* Ask for new features through the [issues](https://github.com/alefiori82/python-amazon-paapi5/issues) section.

Installation
-------------

You can install or upgrade the module with:

    pip install amazon-paapi5 --upgrade

Usage guide
-----------
Basic usage:

    from amazon.paapi import AmazonAPI
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    products = amazon.search_items('harry potter')

Get multiple product information:

    products = amazon.get_items(item_ids=['B01N5IB20Q','B01F9G43WU'])
    print(product[0].image_large)
    print(product[1].prices.price)


Get variations
    products = amazon.get_variations(asin=['B01N5IB20Q','B01F9G43WU'])

Get browse nodes
    browseNodes = amazon.get_browse_nodes(browse_node_ids=['473535031'])

Use cache reader and writer
    DATA = []
    
    def custom_save_function(url, data): 
        DATA.append({'url':url, 'data': data}) 
    
    def custom_retrieval_function(url): 
        for item in DATA: 
            if item["url"] == url: 
                return item['data'] 
        return None
    
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY, CacheReader=custom_retrieval_function, CacheWriter=custom_save_function) 
    products = amazon.search_items('harry potter')


Changelog
-------------

    Version 1.0.0
        - First release
        - CacheReader and Write Reader
        

    
