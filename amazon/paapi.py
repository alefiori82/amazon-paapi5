"""
.. module:: paapi

"""

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
from .exception import AmazonException



def _quote_query(query):
    """Turn a dictionary into a query string in a URL, with keys
    in alphabetical order."""
    return "&".join("%s=%s" % (
        k, urllib_quote(
            str(query[k]).encode('utf-8'), safe='~'))
            for k in sorted(query))

def parse_response_browse_node(browse_nodes_response_list):
    """
    The function parses Browse Nodes Response and creates a dict of BrowseNodeID to AmazonBrowseNode object

    params
        *browse_nodes_response_list*
            List of BrowseNodes in GetBrowseNodes response

    return
        Dict of BrowseNodeID to AmazonBrowseNode object

    """
    mapped_response = {}
    for browse_node in browse_nodes_response_list:
        mapped_response[browse_node.id] = browse_node
    return mapped_response


def parse_response_item(item_response_list):
    """
    The function parses GetItemsResponse and creates a dict of ASIN to AmazonProduct object

    params:
        *item_response_list*
            List of Items in GetItemsResponse

    return
        Dict of ASIN to AmazonProduct object
    """
    mapped_response = {}
    for item in item_response_list:
        mapped_response[item.asin] = item
    return mapped_response


class AmazonAPI:
    """
    Creates an instance containing your API credentials.

    params:
        *access_key (string)*
            Your API key
        *secret_key (string)*
            Your API secret
        *partner_tag (string)*
            The tag you want to use for the URL
        *country (string)*
            Country code
        *throttling (float, optional)*
            Reduce this value to wait longer between API calls
        *CacheReader (function)*
            Write a function to read the stored responses from previous api calls
        *CacheWriter (function)*
            Write a function to save the responses returned by amazon api calls
    
    
    """
    def __init__(self, access_key, secret_key, partner_tag, country='US', throttling=0.9, CacheReader=None, CacheWriter=None):
        """
            init AmazonApi. It is necessary to specify *access_key, secret_key, partner_tag, country* parameters
            By default the throttling parameter is set to 0.9. Increse or descrease this number to manage the time among different calls
            
            params:
                *access_key (string)*
                    amazon key of AWS account
                *secret_key (string)*
                    amazon secret of AWS account
                *partner_tag*
                    tag of the service Amazon Product Advertising account
                *country (string)*
                    possible values are defined in `amazon.constant.REGIONS`
                *throttling (float)*
                    value in the range (0,1] to wait among calls
                *CacheReader (function)*
                    function to read from cache 
                *CacheWriter (function)*
                    function to write results into the cache 

        """
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
        """
            return a url used to identify the call and retrieve it from the cache if CacheReader and CacheWriter are set.
        """
        return self.host + "?" + _quote_query(query)



    
    def search_items(self, actor=None, artist=None,author=None, availability=None, brand=None, browse_node_id=None, condition=None, currency_of_preference=None, delivery_flags=None, item_count=10,item_page=1, keywords=None, languages_of_preference=None, max_price=None, merchant="All", min_price=None,  min_reviews_rating=None, min_saving_percent=None, offer_count=1, search_index="All", sort_by= None,  title=None,  http_info=False, async_req=False, search_items_resource=SEARCH_RESOURCES):
        """ 
        Search products based on keywords
        Choose resources you want from SEARCH_RESOURCES enum 
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter 

        args:
            *actor (string)*
                actor to search products
            *artist (string)*
                artist to search products
            *author (string)*
                author to search products
            *availability (string)*
                availability to search products. Admitted values: "Available", "IncludeOutOfStock"
            *brand* (string, optional)*
                filter the products based on the brand
            *browse_node_id (string)*
                search products into a specific browse node
            *condition* (enum, optional)*
                filter the products based on the condition
            *currency_of_preference (string)*
                Currency of preference in which the prices information should be returned in response. By default the prices are returned in the default currency of the marketplace. Expected currency code format is the ISO 4217 currency code (i.e. USD, EUR etc.)
            *delivery_flags (list of string)*
                The delivery flag filters items which satisfy a certain delivery program promoted by the specific Amazon Marketplace. For example, Prime DeliveryFlag will return items having at least one offer which is Prime Eligible.
            *item_count (integer)*
                number of products returned. Values in the range [1,10]. Default 10
            *item_page (integer)*
                can be used to fetch the specific set/page of items to be returned from the available Search Results. The number of items returned in a page is determined by the item_count parameter. For e.g. if the third set of 5 items (i.e. items numbered 11 to 15) are desired for a search request, you may specify
            *keywords (string)*
                keywords to search products
            *languages_of_preference (list of string)*
                Languages in order of preference in which the item information should be returned in response. By default the item information is returned in the default language of the marketplace.
            *max_price (positive integers)*
                Filters search results to items with at least one offer price below the specified value. Prices appear in lowest currency denomination. For example, in US marketplace, 3241 is $31.41.
            *merchant (string)*
                Filters search results to return items having at least one offer sold by target merchant. By default the value "All" is passed. 
            *min_price (positive integers)*
                Filters search results to items with at least one offer price above the specified value. Prices appear in lowest currency denomination. For example, in US marketplace, 3241 is $32.41.
            *min_reviews_rating (positive integers less than 5)*
                Filters search results to items with customer review ratings above specified value.
            *min_saving_percent (integers less than 100)*
                Filters search results to items with at least one offer having saving percentage above the specified value
            *offer_count (integer)*
                The number of offers desired for each item in the search results. Default: 1
            *search_index (string)*
                search products based on an index. Default value "All"
            *sort_by (string, optional)*
                sort hte results based on the specification defined at https://webservices.amazon.com/paapi5/documentation/search-items.html#sortby-parameter
            *title (string)*
                Title associated with the item. Title searches are subset of Keywords searches. Use a Keywords search if a Title search does not return desired items.
            *http_info (boolean)*
                specify if http header should be returned
            *async_req (boolean)*
                specify if a thread should be created to run the request
            *search_items_resource (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter. By deafult all possible resources are requested
        return
            Dict with 
                *data* 
                    contains the AmazonProduct list
                *http_info*
                    contains the http header information if requested. By default None
        """

        try:
            if item_count > 10 or item_count < 1:
                item_count = 10
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'keywords':keywords,
                'search_index':search_index,
                'item_count':item_count,
                'condition':condition,
                'browse_node_id': browse_node_id,
                'brand': brand,
                'sort_by': sort_by,
                'actor': actor,
                'artist': artist,
                'author': author,
                'availability': availability,
                'currency_of_preference': currency_of_preference,
                'delivery_flags': delivery_flags,
                'item_page': item_page,
                'languages_of_preference': languages_of_preference,
                'max_price': max_price,
                'merchant': merchant,
                'min_price': min_price,
                'min_reviews_rating': min_reviews_rating,
                'min_saving_percent': min_saving_percent,
                'offer_count': offer_count,
                'title': title
                }
            )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': pickle.loads(cached_response_text['data']), 'http_info': pickle.loads(cached_response_text['http_info'])}

            search_items_request = SearchItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                actor=actor,
                artist=artist,
                author=author,
                availability=availability,
                brand=brand,
                browse_node_id=browse_node_id,
                condition=condition,
                currency_of_preference=currency_of_preference,
                delivery_flags=delivery_flags,
                item_count=item_count,
                item_page=item_page,
                keywords=keywords,
                languages_of_preference=languages_of_preference,
                max_price=max_price,
                merchant=merchant,
                min_price=min_price,
                min_reviews_rating=min_reviews_rating,
                min_saving_percent=min_saving_percent,
                offer_count=offer_count,
                resources=search_items_resource,
                search_index=search_index,
                sort_by=sort_by,
                title=title
            )
            
            
        except ValueError as exception:
            #print("Error in forming SearchItemsRequest: ", exception)
            raise AmazonException("ValueError", exception)
        except AmazonException as exception:
            #print("Error in forming SearchItemsRequest: ", exception)
            raise AmazonException(exception.status, exception.reason)

        try:
            """ Sending request """
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None
            if http_info:
                response_with_http_info = self.default_api.search_items_with_http_info(search_items_request)
                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    resp_http = response_with_http_info[2]
                    if response.search_result is not None:
                        resp = [ AmazonProduct(item) for item in response.search_result.items]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                        return {'data': resp, 'http_info': resp_http}
                    if response.errors is not None:
                        #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                        #print("Error code", response.errors[0].code)
                        #print("Error message", response.errors[0].message)
                        raise AmazonException(response.errors[0].code, response.errors[0].message)

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
                        self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                    return {'data': resp, 'http_info': resp_http}
                if response.errors is not None:
                    #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    #print("Error code", response.errors[0].code)
                    #print("Error message", response.errors[0].message)
                    raise AmazonException(response.errors[0].code, response.errors[0].message)

        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)


    
    def search_items_pool(self, actor=None, artist=None,author=None, availability=None, brand=None, browse_node_id=None, condition=None, currency_of_preference=None, delivery_flags=None, item_count=10,item_page=1, keywords=None, languages_of_preference=None, max_price=None, merchant="All", min_price=None,  min_reviews_rating=None, min_saving_percent=None, offer_count=1, search_index="All", sort_by= None,  title=None, search_items_resource=SEARCH_RESOURCES ,connetion_pool_max_size=12):
        """ 
        Search products based on keywords. You can specify max connection pool size here. We recommend a value equal to cpu_count * 5.
        Choose resources you want from SEARCH_RESOURCES enum.
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter 

        args:
            *actor (string)*
                actor to search products
            *artist (string)*
                artist to search products
            *author (string)*
                author to search products
            *availability (string)*
                availability to search products. Admitted values: "Available", "IncludeOutOfStock"
            *brand* (string, optional)*
                filter the products based on the brand
            *browse_node_id (string)*
                search products into a specific browse node
            *condition* (enum, optional)*
                filter the products based on the condition
            *currency_of_preference (string)*
                Currency of preference in which the prices information should be returned in response. By default the prices are returned in the default currency of the marketplace. Expected currency code format is the ISO 4217 currency code (i.e. USD, EUR etc.)
            *delivery_flags (list of string)*
                The delivery flag filters items which satisfy a certain delivery program promoted by the specific Amazon Marketplace. For example, Prime DeliveryFlag will return items having at least one offer which is Prime Eligible.
            *item_count (integer)*
                number of products returned. Values in the range [1,10]. Default 10
            *item_page (integer)*
                can be used to fetch the specific set/page of items to be returned from the available Search Results. The number of items returned in a page is determined by the item_count parameter. For e.g. if the third set of 5 items (i.e. items numbered 11 to 15) are desired for a search request, you may specify
            *keywords (string)*
                keywords to search products
            *languages_of_preference (list of string)*
                Languages in order of preference in which the item information should be returned in response. By default the item information is returned in the default language of the marketplace.
            *max_price (positive integers)*
                Filters search results to items with at least one offer price below the specified value. Prices appear in lowest currency denomination. For example, in US marketplace, 3241 is $31.41.
            *merchant (string)*
                Filters search results to return items having at least one offer sold by target merchant. By default the value "All" is passed. 
            *min_price (positive integers)*
                Filters search results to items with at least one offer price above the specified value. Prices appear in lowest currency denomination. For example, in US marketplace, 3241 is $32.41.
            *min_reviews_rating (positive integers less than 5)*
                Filters search results to items with customer review ratings above specified value.
            *min_saving_percent (integers less than 100)*
                Filters search results to items with at least one offer having saving percentage above the specified value
            *offer_count (integer)*
                The number of offers desired for each item in the search results. Default: 1
            *search_index (string)*
                search products based on an index. Default value "All"
            *sort_by (string, optional)*
                sort hte results based on the specification defined at https://webservices.amazon.com/paapi5/documentation/search-items.html#sortby-parameter
            *title (string)*
                Title associated with the item. Title searches are subset of Keywords searches. Use a Keywords search if a Title search does not return desired items.
            *search_items_resource (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter. By deafult all possible resources are requested
            *connetion_pool_max_size (integer)*
                sice of connection pool. Default 12
        return
            Dict with 
                *data* 
                    contains the AmazonProduct list
                *http_info*
                    contains the http header information if requested. By default None
        """
        
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

            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'keywords':keywords,
                'search_index':search_index,
                'item_count':item_count,
                'condition':condition,
                'browse_node_id': browse_node_id,
                'brand': brand,
                'sort_by': sort_by,
                'actor': actor,
                'artist': artist,
                'author': author,
                'availability': availability,
                'currency_of_preference': currency_of_preference,
                'delivery_flags': delivery_flags,
                'item_page': item_page,
                'languages_of_preference': languages_of_preference,
                'max_price': max_price,
                'merchant': merchant,
                'min_price': min_price,
                'min_reviews_rating': min_reviews_rating,
                'min_saving_percent': min_saving_percent,
                'offer_count': offer_count,
                'title': title
                }
            )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': pickle.loads(cached_response_text['data']), 'http_info': pickle.loads(cached_response_text['http_info'])}

            search_items_request = SearchItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                actor=actor,
                artist=artist,
                author=author,
                availability=availability,
                brand=brand,
                browse_node_id=browse_node_id,
                condition=condition,
                currency_of_preference=currency_of_preference,
                delivery_flags=delivery_flags,
                item_count=item_count,
                item_page=item_page,
                keywords=keywords,
                languages_of_preference=languages_of_preference,
                max_price=max_price,
                merchant=merchant,
                min_price=min_price,
                min_reviews_rating=min_reviews_rating,
                min_saving_percent=min_saving_percent,
                offer_count=offer_count,
                resources=search_items_resource,
                search_index=search_index,
                sort_by=sort_by,
                title=title
            )
            

        except ValueError as exception:
            #print("Error in forming SearchItemsRequest: ", exception)
            raise AmazonException("ValueError", exception)

        try:
            """ Sending request """
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None
            response = default_api.search_items(search_items_request)

            """ Parse response """
            if response.search_result is not None:
                resp = [ AmazonProduct(item) for item in response.search_result.items]
                if self.CacheWriter:
                    self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                return {'data': resp, 'http_info': resp_http}
            if response.errors is not None:
                #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                #print("Error code", response.errors[0].code)
                #print("Error message", response.errors[0].message)
                raise AmazonException(response.errors[0].code, response.errors[0].message)

        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)
            raise Exception(exception)

    """ Choose resources you want from GetVariationsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-variations.html#resources-parameter """
    def get_variations(self, asin, condition=None, currency_of_preference=None, languages_of_preference=None, merchant="All", offer_count=1, variation_count=10, variation_page=1, async_req=False, http_info=False, get_variations_resources=VARIATION_RESOURCES):
        """ 
        Get product variation using the asin of orginal product.
        Choose resources you want from VARIATION_RESOURCES enum.
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-variations.html#request-parameters

        args:
            *asin (string)*
                asin of the product for which we want the variations
            *condition* (enum, optional)*
                filter the products based on the condition
            *currency_of_preference (string)*
                specify the currency of returned results
            *languages_of_preference (list of string)*
                specify the language of returned results
            *merchant (string)*
                Filters search results to return items having at least one offer sold by target merchant. By default the value "All" is passed. 
            *offer_count (integer)*
                The number of offers desired for each item in the search results. Default: 1
            *variation_count (integer)*
                Number of variations to be returned per page. Default: 10
            *variation_page (integer)*
                Page number of variations returned by get_variations. Default: 1 
            *http_info (boolean)*
                specify if http header should be returned
            *async_req (boolean)*
                specify if a thread should be created to run the request
            *get_variations_resources (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-variations.html#request-parameters. By deafult all possible resources are requested
            
        return
            Dict with 
                *data* 
                    contains the AmazonProduct list
                *http_info*
                    contains the http header information if requested. By default None
        """
        try:
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'asin':asin,
                'condition': condition,
                'currency_of_preference': currency_of_preference,
                'languages_of_preference':languages_of_preference,
                'merchant':merchant,
                'offer_count': offer_count,
                'variation_count': variation_count,
                'variation_page': variation_page
                }
            )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': pickle.loads(cached_response_text['data']), 'http_info': pickle.loads(cached_response_text['http_info'])}

            get_variations_request = GetVariationsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                asin=asin,
                condition=condition,
                currency_of_preference=currency_of_preference,
                languages_of_preference=languages_of_preference,
                merchant=merchant,
                offer_count=offer_count,
                variation_count=variation_count,
                variation_page=variation_page,
                resources=get_variations_resources
            )
            
        except ValueError as exception:
            #print("Error in forming GetVariationsRequest: ", exception)
            raise AmazonException("ValueError", exception)

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None
            """ Sending request """
            if http_info:
                response_with_http_info = self.default_api.get_variations_with_http_info(get_variations_request)

                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    resp_http = response_with_http_info[2]
                    if response.variations_result is not None:
                        resp = [ AmazonProduct(item) for item in response.variations_result.items]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                        return {'data': resp, 'http_info': resp_http}

                    if response.errors is not None:
                        #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                        #print("Error code", response.errors[0].code)
                        #print("Error message", response.errors[0].message)
                        raise AmazonException(response.errors[0].code, response.errors[0].message)
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
                        self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                    return {'data': resp, 'http_info': resp_http}

                if response.errors is not None:
                    #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    #print("Error code", response.errors[0].code)
                    #print("Error message", response.errors[0].message)
                    raise AmazonException(response.errors[0].code, response.errors[0].message)

        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)


    """ Choose resources you want from GetItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-items.html#resources-parameter """
    def get_items(self, item_ids=[], condition=None, currency_of_preference=None, item_id_type="ASIN",languages_of_preference=None, merchant="All", offer_count=1, http_info=False, async_req=False, get_items_resource=ITEM_RESOURCES):
        """ 
        Get items' information.
        Choose resources you want from ITEM_RESOURCES enum 
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-items.html#ItemLookup-rp

        args:
            *item_ids (list of string)*
                list of asin of the products of interest
            *condition* (enum, optional)*
                filter the products based on the condition
            *currency_of_preference (string)*
                specify the currency of returned results
            *item_id_type (string)*
                Type of item identifier used to look up an item. Default: ASIN
            *languages_of_preference (list of string)*
                Languages in order of preference in which the item information should be returned in response. By default the item information is returned in the default language of the marketplace
            *merchant (string)*
                Filters search results to return items having at least one offer sold by target merchant. By default the value "All" is passed. 
            *offer_count (integer)*
                The number of offers desired for each item in the search results. Default: 1
            *http_info (boolean)*
                specify if http header should be returned
            *async_req (boolean)*
                specify if a thread should be created to run the request
            *get_items_resource (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-items.html#ItemLookup-rp. By deafult all possible resources are requested
            
        return
            Dict with 
                *data* 
                    Dict of ASIN to AmazonProduct object
                *http_info*
                    contains the http header information if requested. By default None
        """
        
        if len(item_ids) == 0:
            raise Exception('No item ids specified')
        
        """ Forming request """
        try:
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'item_ids':item_ids,    
                'condition':condition,
                'currency_of_preference': currency_of_preference,
                'item_id_type': item_id_type,
                'languages_of_preference': languages_of_preference,
                'merchant': merchant,
                'offer_count': offer_count
                }
            )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': parse_response_item( pickle.loads(cached_response_text['data']) ), 'http_info': pickle.loads(cached_response_text['http_info'])}

            get_items_request = GetItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                item_ids=item_ids,
                condition=condition,
                currency_of_preference=currency_of_preference,
                item_id_type=item_id_type,
                languages_of_preference=languages_of_preference,
                merchant=merchant,
                offer_count=offer_count,
                resources=get_items_resource
            )
            

        except ValueError as exception:
            #print("Error in forming GetItemsRequest: ", exception)
            raise AmazonException("ValueError", exception)

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None

            if http_info:
                response_with_http_info = self.default_api.get_items_with_http_info(
                    get_items_request
                )

                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    resp_http = response_with_http_info[2]
                    if response.items_result is not None:
                        resp = [ AmazonProduct(item) for item in response.items_result.items]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                        return {'data': parse_response_item(resp), 'http_info': resp_http}
                        
                    if response.errors is not None:
                        #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                        #print("Error code", response.errors[0].code)
                        #print("Error message", response.errors[0].message)
                        raise AmazonException(response.errors[0].code, response.errors[0].message)

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
                        self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                    return {'data': parse_response_item(resp), 'http_info': resp_http}

                if response.errors is not None:
                    #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    #print("Error code", response.errors[0].code)
                    #print("Error message", response.errors[0].message)
                    raise AmazonException(response.errors[0].code, response.errors[0].message)


        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)



    """ Choose resources you want from GetBrowseNodesResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/getbrowsenodes.html#resources-parameter """
    def get_browse_nodes(self, browse_node_ids=[], languages_of_preference = None, http_info=False, async_req=False, get_browse_node_resources=BROWSE_RESOURCES):
        """" 
        Get browse nodes' information.
        Choose resources you want from BROWSE_RESOURCES enum 
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/getbrowsenodes.html#request-parameters

        args:
            *browse_node_ids (list of string)*
                list of browse node ids
            *languages_of_preference (list of string)*
                specify the language of returned results
            *http_info (boolean)*
                specify if http header should be returned
            *async_req (boolean)*
                specify if a thread should be created to run the request
            
            *get_browse_node_resources (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/getbrowsenodes.html#request-parameters. By deafult all possible resources are requested
            
        return
            Dict with 
                *data* 
                    Dict of BrowseNodeID to AmazonBrowseNode object
                *http_info*
                    contains the http header information if requested. By default None
        """
        
        if isinstance(browse_node_ids, list) == False or len (browse_node_ids) == 0:
            raise Exception('Browse node ids are not in the right format')
        
        """ Forming request """
        try:
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'browse_node_ids':browse_node_ids,
                'languages_of_preference':languages_of_preference }
                )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': parse_response_browse_node (pickle.loads(cached_response_text['data']) ), 'http_info': pickle.loads(cached_response_text['http_info'])}

            get_browse_node_request = GetBrowseNodesRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                languages_of_preference=languages_of_preference,
                browse_node_ids=browse_node_ids,
                resources=get_browse_node_resources,
            )
            
        except ValueError as exception:
            #print("Error in forming GetBrowseNodesRequest: ", exception)
            raise AmazonException("ValueError", exception)

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None

            if http_info:
                response_with_http_info = self.default_api.get_browse_nodes_with_http_info(get_browse_node_request)

                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    resp_http = response_with_http_info[2]
                    if response.browse_nodes_result is not None:
                        resp = [ AmazonBrowseNode(node) for node in response.browse_nodes_result.browse_nodes]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                        return {'data': parse_response_browse_node(resp), 'http_info': resp_http}
                        
                    if response.errors is not None:
                        #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                        #print("Error code", response.errors[0].code)
                        #print("Error message", response.errors[0].message)
                        raise AmazonException(response.errors[0].code, response.errors[0].message)

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
                        self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                    return {'data': parse_response_browse_node(resp), 'http_info': resp_http}
                    
                if response.errors is not None:
                    #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    #print("Error code", response.errors[0].code)
                    #print("Error message", response.errors[0].message)
                    raise AmazonException(response.errors[0].code, response.errors[0].message)

        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)
