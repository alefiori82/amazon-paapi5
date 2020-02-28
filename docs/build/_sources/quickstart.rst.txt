Quick start
***********



Installation
============

You can install or upgrade the module with:

``pip install amazon-paapi5 --upgrade``

Basic Usage
===========

Search items::

    from amazon.paapi import AmazonAPI
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    products = amazon.search_items('harry potter')
    print(product['data'][0].image_large)
    print(product['data'][1].prices.price)

Get multiple products information::

    from amazon.paapi import AmazonAPI
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    products = amazon.get_items(item_ids=['B01N5IB20Q','B01F9G43WU'])
    print(products['data']['B01N5IB20Q'].image_large)
    print(products['data']['B01F9G43WU'].prices.price)


Get variations::

    from amazon.paapi import AmazonAPI
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    products = amazon.get_variations(asin=['B01N5IB20Q','B01F9G43WU'])

Get browse nodes::

    from amazon.paapi import AmazonAPI
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    browseNodes = amazon.get_browse_nodes(browse_node_ids=['473535031'])

Use cache reader and writer::

    from amazon.paapi import AmazonAPI

    DATA = []
    
    def custom_save_function(url, data, http_info):  
        DATA.append({'url':url, 'data': data, 'http_info':http_info}) 
    
    def custom_retrieval_function(url):  
        for item in DATA:  
            if item["url"] == url: 
                return {'data':item['data'], 'http_info': item['http_info']}  
        return None
    
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY, CacheReader=custom_retrieval_function, CacheWriter=custom_save_function) 
    products = amazon.search_items('harry potter')


