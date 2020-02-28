"""
.. module:: entities

"""

import pprint
import six
from paapi5_python_sdk.item import Item
from paapi5_python_sdk.browse_node import BrowseNode

class AmazonProduct():
    """
        Class representing a product
    """

    swagger_types = {
        'asin': 'str',
        'browse_node_info': 'BrowseNodeInfo',
        'detail_page_url': 'str',
        'images': 'Images',
        'item_info': 'ItemInfo',
        'offers': 'Offers',
        'parent_asin': 'str',
        'rental_offers': 'RentalOffers',
        'score': 'float',
        'variation_attributes': 'list[VariationAttribute]'
    }

    def __init__(self, item):
        self.asin = item.asin
        self.browse_node_info = item.browse_node_info
        self.detail_page_url = item.detail_page_url
        self.images = item.images
        self.item_info = item.item_info
        self.offers = item.offers
        self.parent_asin = item.parent_asin
        self.rental_offers = item.rental_offers
        self.score = item.score
        self.variation_attributes = item.variation_attributes

    
    @property
    def isDiscount(self):
        """
            return if the best offer has a discount
        """
        if self.bestOffer.price.savings:
            return True
        return False
    
    @property
    def bestOffer(self):
        """
            return best offer information
        """
        bestOffer = None
        if self.offers:
            if isinstance(self.offers.listings, list):
                for offer in self.offers.listings:
                    if bestOffer == None:
                        bestOffer = offer
                    else:
                        if bestOffer.price.amount < offer.price.amount:
                            bestOffer = offer
            else:
                bestOffer = self.offers.listings

        return bestOffer

    @property
    def originalPrice(self):
        """
            return the price without discount
        """
        if self.bestOffer.saving_basis:
            return self.bestOffer.saving_basis
        else:
            return self.bestOffer.price


    @property
    def isPrime(self):
        """
            return if the best offer is Prime eligible
        """
        if self.bestOffer.delivery_info.is_prime_eligible != None:
            return self.bestOffer.delivery_info.is_prime_eligible
        return False
    
    @property
    def isFreeShipping(self):
        """
            return if the best offer is free shipping eligible
        """
        if self.bestOffer.delivery_info.is_free_shipping_eligible != None:
            return self.bestOffer.delivery_info.is_free_shipping_eligible
        return False

    @property
    def isAmazonFulfilled(self):
        """
            return if the best offer is amazon fulfilled
        """
        if self.bestOffer.delivery_info.is_amazon_fulfilled != None:
            return self.bestOffer.delivery_info.is_amazon_fulfilled
        return False
        
    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Item, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Item):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

class AmazonBrowseNode():
    """
        Class representing a browse node
    """
    swagger_types = {
        'ancestor': 'BrowseNodeAncestor',
        'children': 'BrowseNodeChildren',
        'context_free_name': 'str',
        'display_name': 'str',
        'id': 'str',
        'is_root': 'bool',
        'sales_rank': 'int'
    }

    def __init__(self, node):
        self.ancestor = node.ancestor 
        self.children = node.children
        self.context_free_name = node.context_free_name
        self.display_name = node.display_name
        self.id = node.id
        self.is_root = node.is_root
        self.sales_rank = node.sales_rank

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(BrowseNode, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BrowseNode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other


