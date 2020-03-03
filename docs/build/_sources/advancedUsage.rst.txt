Advanced Usage
**************


HTTP header information
=======================


For all the functions (``search_items``, ``get_items``, ``get_variations``, ``get_browse_nodes``) you can retrieve the http header 

Example to retrieve the http info returned by a request::

    from amazon.paapi import AmazonAPI
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    products = amazon.search_items(keywords='harry potter', http_info=True)
    print(products['data'][1].prices.price)
    print (products['http_info'])


Async requests
==============

It is possible to run requests with a separate thread. In the following an example of async request::

    from amazon.paapi import AmazonAPI
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    products = amazon.get_items(item_ids=['B01N5IB20Q','B01F9G43WU'], async_req=True)
    print(products['data']['B01N5IB20Q'].image_large)
    print(products['data']['B01F9G43WU'].prices.price)


.. note:: 
    Async requests do not return the http header information


Pool requests
=============


It is possible to search items using a connetion pool using the function ``search_items_pool(keywords, connetion_pool_max_size=10)`` specify the max connection pool size with the parameter ``connetion_pool_max_size``. We recommend a value equal to cpu_count * 5.
In the folllowing an example::

    from amazon.paapi import AmazonAPI
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    products = amazon.search_items_pool(keywords='harry potter', connetion_pool_max_size=10)
    print(products['data'][1].prices.price)

