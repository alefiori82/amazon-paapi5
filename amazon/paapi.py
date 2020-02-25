"""Amazon Product Advertising API 5.0 wrapper for Python"""

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.api_client import ApiClient
from paapi5_python_sdk.configuration import Configuration
from paapi5_python_sdk.partner_type import PartnerType
from paapi5_python_sdk.condition import Condition

from paapi5_python_sdk.rest import ApiException


from paapi5_python_sdk.get_items_request import GetItemsRequest
from paapi5_python_sdk.get_items_resource import GetItemsResource
from paapi5_python_sdk.search_items_request import SearchItemsRequest
from paapi5_python_sdk.search_items_resource import SearchItemsResource
from paapi5_python_sdk.get_variations_request import GetVariationsRequest
from paapi5_python_sdk.get_variations_resource import GetVariationsResource
from paapi5_python_sdk.get_browse_nodes_request import GetBrowseNodesRequest
from paapi5_python_sdk.get_browse_nodes_resource import GetBrowseNodesResource

from paapi5_python_sdk.item import Item


import time, json, pickle
from urllib.parse import quote as urllib_quote


REGIONS = {
    'AU': 'us-west-2',
    'BR': 'us-east-1',
    'CA': 'us-east-1',
    'FR': 'eu-west-1',
    'DE': 'eu-west-1',
    'IN': 'eu-west-1',
    'IT': 'eu-west-1',
    'JP': 'us-west-2',
    'MX': 'us-east-1',
    'ES': 'eu-west-1',
    'TR': 'eu-west-1',
    'AE': 'eu-west-1',
    'UK': 'eu-west-1',
    'US': 'us-east-1'
}
DOMAINS = {
    'AU': 'com.au',
    'BR': 'com.br',
    'CA': 'ca',
    'FR': 'fr',
    'DE': 'de',
    'IN': 'in',
    'IT': 'it',
    'JP': 'co.jp',
    'MX': 'com.mx',
    'ES': 'es',
    'TR': 'com.tr',
    'AE': 'ae',
    'UK': 'co.uk',
    'US': 'com'
}

ITEM_RESOURCES = [
    GetItemsResource.BROWSENODEINFO_BROWSENODES,
    GetItemsResource.BROWSENODEINFO_BROWSENODES_ANCESTOR,
    GetItemsResource.BROWSENODEINFO_BROWSENODES_SALESRANK,
    GetItemsResource.BROWSENODEINFO_WEBSITESALESRANK,
    GetItemsResource.IMAGES_PRIMARY_SMALL,
    GetItemsResource.IMAGES_PRIMARY_MEDIUM,
    GetItemsResource.IMAGES_PRIMARY_LARGE,
    GetItemsResource.IMAGES_VARIANTS_SMALL,
    GetItemsResource.IMAGES_VARIANTS_MEDIUM,
    GetItemsResource.IMAGES_VARIANTS_LARGE,
    GetItemsResource.ITEMINFO_BYLINEINFO,
    GetItemsResource.ITEMINFO_CONTENTINFO,
    GetItemsResource.ITEMINFO_CONTENTRATING,
    GetItemsResource.ITEMINFO_CLASSIFICATIONS,
    GetItemsResource.ITEMINFO_EXTERNALIDS,
    GetItemsResource.ITEMINFO_FEATURES,
    GetItemsResource.ITEMINFO_MANUFACTUREINFO,
    GetItemsResource.ITEMINFO_PRODUCTINFO,
    GetItemsResource.ITEMINFO_TECHNICALINFO,
    GetItemsResource.ITEMINFO_TITLE,
    GetItemsResource.ITEMINFO_TRADEININFO,
    GetItemsResource.OFFERS_LISTINGS_AVAILABILITY_MAXORDERQUANTITY,
    GetItemsResource.OFFERS_LISTINGS_AVAILABILITY_MESSAGE,
    GetItemsResource.OFFERS_LISTINGS_AVAILABILITY_MINORDERQUANTITY,
    GetItemsResource.OFFERS_LISTINGS_AVAILABILITY_TYPE,
    GetItemsResource.OFFERS_LISTINGS_CONDITION,
    GetItemsResource.OFFERS_LISTINGS_CONDITION_SUBCONDITION,
    GetItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
    GetItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
    GetItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
    GetItemsResource.OFFERS_LISTINGS_DELIVERYINFO_SHIPPINGCHARGES,
    GetItemsResource.OFFERS_LISTINGS_ISBUYBOXWINNER,
    GetItemsResource.OFFERS_LISTINGS_LOYALTYPOINTS_POINTS,
    GetItemsResource.OFFERS_LISTINGS_MERCHANTINFO,
    GetItemsResource.OFFERS_LISTINGS_PRICE,
    GetItemsResource.OFFERS_LISTINGS_PROGRAMELIGIBILITY_ISPRIMEEXCLUSIVE,
    GetItemsResource.OFFERS_LISTINGS_PROGRAMELIGIBILITY_ISPRIMEPANTRY,
    GetItemsResource.OFFERS_LISTINGS_PROMOTIONS,
    GetItemsResource.OFFERS_LISTINGS_SAVINGBASIS,
    GetItemsResource.OFFERS_SUMMARIES_HIGHESTPRICE,
    GetItemsResource.OFFERS_SUMMARIES_LOWESTPRICE,
    GetItemsResource.OFFERS_SUMMARIES_OFFERCOUNT,
    GetItemsResource.PARENTASIN,
    GetItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MAXORDERQUANTITY,
    GetItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MESSAGE,
    GetItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MINORDERQUANTITY,
    GetItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_TYPE,
    GetItemsResource.RENTALOFFERS_LISTINGS_BASEPRICE,
    GetItemsResource.RENTALOFFERS_LISTINGS_CONDITION,
    GetItemsResource.RENTALOFFERS_LISTINGS_CONDITION_SUBCONDITION,
    GetItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
    GetItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
    GetItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
    GetItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_SHIPPINGCHARGES,
    GetItemsResource.RENTALOFFERS_LISTINGS_MERCHANTINFO]

SEARCH_RESOURCES = [
    SearchItemsResource.BROWSENODEINFO_BROWSENODES,
    SearchItemsResource.BROWSENODEINFO_BROWSENODES_ANCESTOR,
    SearchItemsResource.BROWSENODEINFO_BROWSENODES_SALESRANK,
    SearchItemsResource.BROWSENODEINFO_WEBSITESALESRANK,
    SearchItemsResource.IMAGES_PRIMARY_SMALL,
    SearchItemsResource.IMAGES_PRIMARY_MEDIUM,
    SearchItemsResource.IMAGES_PRIMARY_LARGE,
    SearchItemsResource.IMAGES_VARIANTS_SMALL,
    SearchItemsResource.IMAGES_VARIANTS_MEDIUM,
    SearchItemsResource.IMAGES_VARIANTS_LARGE,
    SearchItemsResource.ITEMINFO_BYLINEINFO,
    SearchItemsResource.ITEMINFO_CONTENTINFO,
    SearchItemsResource.ITEMINFO_CONTENTRATING,
    SearchItemsResource.ITEMINFO_CLASSIFICATIONS,
    SearchItemsResource.ITEMINFO_EXTERNALIDS,
    SearchItemsResource.ITEMINFO_FEATURES,
    SearchItemsResource.ITEMINFO_MANUFACTUREINFO,
    SearchItemsResource.ITEMINFO_PRODUCTINFO,
    SearchItemsResource.ITEMINFO_TECHNICALINFO,
    SearchItemsResource.ITEMINFO_TITLE,
    SearchItemsResource.ITEMINFO_TRADEININFO,
    SearchItemsResource.OFFERS_LISTINGS_AVAILABILITY_MAXORDERQUANTITY,
    SearchItemsResource.OFFERS_LISTINGS_AVAILABILITY_MESSAGE,
    SearchItemsResource.OFFERS_LISTINGS_AVAILABILITY_MINORDERQUANTITY,
    SearchItemsResource.OFFERS_LISTINGS_AVAILABILITY_TYPE,
    SearchItemsResource.OFFERS_LISTINGS_CONDITION,
    SearchItemsResource.OFFERS_LISTINGS_CONDITION_SUBCONDITION,
    SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
    SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
    SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
    SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_SHIPPINGCHARGES,
    SearchItemsResource.OFFERS_LISTINGS_ISBUYBOXWINNER,
    SearchItemsResource.OFFERS_LISTINGS_LOYALTYPOINTS_POINTS,
    SearchItemsResource.OFFERS_LISTINGS_MERCHANTINFO,
    SearchItemsResource.OFFERS_LISTINGS_PRICE,
    SearchItemsResource.OFFERS_LISTINGS_PROGRAMELIGIBILITY_ISPRIMEEXCLUSIVE,
    SearchItemsResource.OFFERS_LISTINGS_PROGRAMELIGIBILITY_ISPRIMEPANTRY,
    SearchItemsResource.OFFERS_LISTINGS_PROMOTIONS,
    SearchItemsResource.OFFERS_LISTINGS_SAVINGBASIS,
    SearchItemsResource.OFFERS_SUMMARIES_HIGHESTPRICE,
    SearchItemsResource.OFFERS_SUMMARIES_LOWESTPRICE,
    SearchItemsResource.OFFERS_SUMMARIES_OFFERCOUNT,
    SearchItemsResource.PARENTASIN,
    SearchItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MAXORDERQUANTITY,
    SearchItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MESSAGE,
    SearchItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MINORDERQUANTITY,
    SearchItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_TYPE,
    SearchItemsResource.RENTALOFFERS_LISTINGS_BASEPRICE,
    SearchItemsResource.RENTALOFFERS_LISTINGS_CONDITION,
    SearchItemsResource.RENTALOFFERS_LISTINGS_CONDITION_SUBCONDITION,
    SearchItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
    SearchItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
    SearchItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
    SearchItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_SHIPPINGCHARGES,
    SearchItemsResource.RENTALOFFERS_LISTINGS_MERCHANTINFO,
    SearchItemsResource.SEARCHREFINEMENTS
]

VARIATION_RESOURCES = [
    GetVariationsResource.BROWSENODEINFO_BROWSENODES,
    GetVariationsResource.BROWSENODEINFO_BROWSENODES_ANCESTOR,
    GetVariationsResource.BROWSENODEINFO_BROWSENODES_SALESRANK,
    GetVariationsResource.BROWSENODEINFO_WEBSITESALESRANK,
    GetVariationsResource.IMAGES_PRIMARY_SMALL,
    GetVariationsResource.IMAGES_PRIMARY_MEDIUM,
    GetVariationsResource.IMAGES_PRIMARY_LARGE,
    GetVariationsResource.IMAGES_VARIANTS_SMALL,
    GetVariationsResource.IMAGES_VARIANTS_MEDIUM,
    GetVariationsResource.IMAGES_VARIANTS_LARGE,
    GetVariationsResource.ITEMINFO_BYLINEINFO,
    GetVariationsResource.ITEMINFO_CONTENTINFO,
    GetVariationsResource.ITEMINFO_CONTENTRATING,
    GetVariationsResource.ITEMINFO_CLASSIFICATIONS,
    GetVariationsResource.ITEMINFO_EXTERNALIDS,
    GetVariationsResource.ITEMINFO_FEATURES,
    GetVariationsResource.ITEMINFO_MANUFACTUREINFO,
    GetVariationsResource.ITEMINFO_PRODUCTINFO,
    GetVariationsResource.ITEMINFO_TECHNICALINFO,
    GetVariationsResource.ITEMINFO_TITLE,
    GetVariationsResource.ITEMINFO_TRADEININFO,
    GetVariationsResource.OFFERS_LISTINGS_AVAILABILITY_MAXORDERQUANTITY,
    GetVariationsResource.OFFERS_LISTINGS_AVAILABILITY_MESSAGE,
    GetVariationsResource.OFFERS_LISTINGS_AVAILABILITY_MINORDERQUANTITY,
    GetVariationsResource.OFFERS_LISTINGS_AVAILABILITY_TYPE,
    GetVariationsResource.OFFERS_LISTINGS_CONDITION,
    GetVariationsResource.OFFERS_LISTINGS_CONDITION_SUBCONDITION,
    GetVariationsResource.OFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
    GetVariationsResource.OFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
    GetVariationsResource.OFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
    GetVariationsResource.OFFERS_LISTINGS_DELIVERYINFO_SHIPPINGCHARGES,
    GetVariationsResource.OFFERS_LISTINGS_ISBUYBOXWINNER,
    GetVariationsResource.OFFERS_LISTINGS_LOYALTYPOINTS_POINTS,
    GetVariationsResource.OFFERS_LISTINGS_MERCHANTINFO,
    GetVariationsResource.OFFERS_LISTINGS_PRICE,
    GetVariationsResource.OFFERS_LISTINGS_PROGRAMELIGIBILITY_ISPRIMEEXCLUSIVE,
    GetVariationsResource.OFFERS_LISTINGS_PROGRAMELIGIBILITY_ISPRIMEPANTRY,
    GetVariationsResource.OFFERS_LISTINGS_PROMOTIONS,
    GetVariationsResource.OFFERS_LISTINGS_SAVINGBASIS,
    GetVariationsResource.OFFERS_SUMMARIES_HIGHESTPRICE,
    GetVariationsResource.OFFERS_SUMMARIES_LOWESTPRICE,
    GetVariationsResource.OFFERS_SUMMARIES_OFFERCOUNT,
    GetVariationsResource.PARENTASIN,
    GetVariationsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MAXORDERQUANTITY,
    GetVariationsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MESSAGE,
    GetVariationsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MINORDERQUANTITY,
    GetVariationsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_TYPE,
    GetVariationsResource.RENTALOFFERS_LISTINGS_BASEPRICE,
    GetVariationsResource.RENTALOFFERS_LISTINGS_CONDITION,
    GetVariationsResource.RENTALOFFERS_LISTINGS_CONDITION_SUBCONDITION,
    GetVariationsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
    GetVariationsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
    GetVariationsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
    GetVariationsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_SHIPPINGCHARGES,
    GetVariationsResource.RENTALOFFERS_LISTINGS_MERCHANTINFO,
    GetVariationsResource.VARIATIONSUMMARY_PRICE_HIGHESTPRICE,
    GetVariationsResource.VARIATIONSUMMARY_PRICE_LOWESTPRICE,
    GetVariationsResource.VARIATIONSUMMARY_VARIATIONDIMENSION
]

BROWSE_RESOURCES = [
    GetBrowseNodesResource.ANCESTOR,
    GetBrowseNodesResource.CHILDREN
]

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
    def search_items(self, keywords, http_info=False, async_req=False, search_index="All", condition=None, item_count=10, 
        search_items_resource=SEARCH_RESOURCES):
        """ Forming request """
        try:
            search_items_request = SearchItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                keywords=keywords,
                search_index=search_index,
                item_count=item_count,
                resources=search_items_resource,
                condition=condition
            )
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'keywords':keywords,
                'search_index':search_index,
                'item_count':item_count,
                'condition':condition  }
                )
            #print (cache_url)
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return pickle.loads(cached_response_text)
            
        except ValueError as exception:
            print("Error in forming SearchItemsRequest: ", exception)
            return

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
                    print("API called Successfully")
                    #print("Complete Response Dump:", response_with_http_info)
                    print("HTTP Info:", response_with_http_info[2])

                    response = response_with_http_info[0]
                    if response.search_result is not None:
                        return response.search_result.items
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
                    if self.CacheWriter:
                        self.CacheWriter(cache_url, pickle.dumps(response.search_result.items))
                    return response.search_result.items
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

        except TypeError as exception:
            print("TypeError :", exception)

        except ValueError as exception:
            print("ValueError :", exception)

        except Exception as exception:
            print("Exception :", exception)


    """ Choose resources you want from SearchItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter """
    def search_items_pool(self, keywords, search_index="All", item_count=10, search_items_resource=SEARCH_RESOURCES ,connetion_pool_max_size=12, condition=None):
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
            search_items_request = SearchItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                keywords=keywords,
                search_index=search_index,
                item_count=item_count,
                resources=search_items_resource,
                condition=condition
            )
        except ValueError as exception:
            print("Error in forming SearchItemsRequest: ", exception)
            return

        try:
            """ Sending request """
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            response = default_api.search_items(search_items_request)

            print("API called Successfully")
            #print("Complete Response:", response)

            """ Parse response """
            if response.search_result is not None:
                return response.search_result.items
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

        except TypeError as exception:
            print("TypeError :", exception)

        except ValueError as exception:
            print("ValueError :", exception)

        except Exception as exception:
            print("Exception :", exception)

    """ Choose resources you want from GetVariationsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-variations.html#resources-parameter """
    def get_variations(self, asin, http_info=False, async_req=False, languages_of_preference=["es_US"], get_variations_resources=VARIATION_RESOURCES):
        """ Forming request """
        try:
            get_variations_request = GetVariationsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                languages_of_preference=languages_of_preference,
                asin=asin,
                resources=get_variations_resources,
            )
        except ValueError as exception:
            print("Error in forming GetVariationsRequest: ", exception)
            return

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            """ Sending request """
            if http_info:
                response_with_http_info = self.default_api.get_variations_with_http_info(
                    get_variations_request
                )

                """ Parse response """
                if response_with_http_info is not None:
                    print("API called Successfully")
                    #print("Complete Response Dump:", response_with_http_info)
                    print("HTTP Info:", response_with_http_info[2])

                    response = response_with_http_info[0]
                    if response.variations_result is not None:
                        print("Printing VariationSummary:")
                        if (
                            response.variations_result.variation_summary is not None
                            and response.variations_result.variation_summary.variation_count
                            is not None
                        ):
                            print(
                                "VariationCount: ",
                                response.variations_result.variation_summary.variation_count,
                            )
                        
                        return response.variations_result.items

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

                print("API called Successfully")
                #print("Complete Response:", response)

                """ Parse response """
                if response.variations_result is not None:
                    print("Printing VariationSummary:")
                    if (
                        response.variations_result.variation_summary is not None
                        and response.variations_result.variation_summary.variation_count
                        is not None
                    ):
                        print(
                            "VariationCount: ",
                            response.variations_result.variation_summary.variation_count,
                        )

                    print("Printing first item information in VariationsResult:")
                    return response.variations_result.items

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

        except TypeError as exception:
            print("TypeError :", exception)

        except ValueError as exception:
            print("ValueError :", exception)

        except Exception as exception:
            print("Exception :", exception)


    """ Choose resources you want from GetItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-items.html#resources-parameter """
    def get_items(self, item_ids=[], http_info=False, async_req=False, get_items_resource=ITEM_RESOURCES, condition=None):
        
        """ Choose item id(s) """
        try:
            if len(item_ids) == 0:
                raise Exception('No item ids specified')
        except Exception as e:
            print (e)
            return

        """ Forming request """

        try:
            get_items_request = GetItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                condition=condition,
                item_ids=item_ids,
                resources=get_items_resource,
            )
        except ValueError as exception:
            print("Error in forming GetItemsRequest: ", exception)
            return

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
                    print("API called Successfully")
                    #print("Complete Response Dump:", response_with_http_info)
                    print("HTTP Info:", response_with_http_info[2])

                    response = response_with_http_info[0]
                    if response.items_result is not None:
                        print("Printing all item information in ItemsResult:")
                        return parse_response(response.items_result.items)
                        
                    if response.errors is not None:
                        print(
                            "\nPrinting Errors:\nPrinting First Error Object from list of Errors"
                        )
                        print("Error code", response.errors[0].code)
                        print("Error message", response.errors[0].message)

            else:
                """ Sending request """
                if async_req:
                    thread = self.default_api.get_items(get_items_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.get_items(get_items_request)

                print("API called Successfully")
                #print("Complete Response:", response)

                """ Parse response """
                if response.items_result is not None:
                    print("Printing all item information in ItemsResult:")
                    return parse_response(response.items_result.items)

                if response.errors is not None:
                    print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    print("Error code", response.errors[0].code)
                    print("Error message", response.errors[0].message)


        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])

        except TypeError as exception:
            print("TypeError :", exception)

        except ValueError as exception:
            print("ValueError :", exception)

        except Exception as exception:
            print("Exception :", exception)



    """ Choose resources you want from GetBrowseNodesResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/getbrowsenodes.html#resources-parameter """
    def get_browse_nodes(self, browse_node_ids=[], http_info=False, async_req=False, languages_of_preference = ["es_US"], get_browse_node_resources=BROWSE_RESOURCES):

        """ Specify browse_node id(s) """
        try:
            if len (browse_node_ids) == 0:
                raise Exception('No browse node ids specified')
        except Exception as e:
            print (e)
            return

        
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
        except ValueError as exception:
            print("Error in forming GetBrowseNodesRequest: ", exception)
            return

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            if http_info:
                response_with_http_info = self.default_api.get_browse_nodes_with_http_info(
                    get_browse_node_request
                )

                """ Parse response """
                if response_with_http_info is not None:
                    print("API called Successfully")
                    #print("Complete Response Dump:", response_with_http_info)
                    print("HTTP Info:", response_with_http_info[2])

                    response = response_with_http_info[0]
                    if response.browse_nodes_result is not None:
                        print("Printing all browse node information in BrowseNodesResult:")
                        return parse_response_browse_node(
                            response.browse_nodes_result.browse_nodes
                        )
                        
                    if response.errors is not None:
                        print(
                            "\nPrinting Errors:\nPrinting First Error Object from list of Errors"
                        )
                        print("Error code", response.errors[0].code)
                        print("Error message", response.errors[0].message)

            else:
                """ Sending request """
                if async_req:
                    thread = self.default_api.get_browse_nodes(get_browse_node_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.get_browse_nodes(get_browse_node_request)

                print("API called Successfully")
                #print("Complete Response:\n", response)

                """ Parse response """
                if response.browse_nodes_result is not None:
                    print("Printing all browse node information in BrowseNodesResult:")
                    return parse_response_browse_node(response.browse_nodes_result.browse_nodes)
                    
                if response.errors is not None:
                    print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    print("Error code", response.errors[0].code)
                    print("Error message", response.errors[0].message)

        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])

        except TypeError as exception:
            print("TypeError :", exception)

        except ValueError as exception:
            print("ValueError :", exception)

        except Exception as exception:
            print("Exception :", exception)
