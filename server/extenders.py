from sortedcontainers import SortedListWithKey

class Extenders(object):
    """ A class which provides static methods for extending entity properties """
    @staticmethod
    def InitializeExtendedShop(shop):
        """ Extends a shop entity by initializing its 'tags' (as a set) and 'products' (as a descendingly SortedList according to product popularity) properties """
        shop.tags = set()
        shop.products = SortedListWithKey(key=lambda val: -1*float(val.popularity))
        return shop

    