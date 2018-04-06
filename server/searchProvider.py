from shopLocation import ShopLocation
from shopProduct import ShopProduct
from sortedcontainers import SortedListWithKey

class SearchProvider(object):
    """ A class which provides a higher level abstraction for the search functionality 
        Use an instance of this class to execute search requests.
    """

    def __init__(self, locator):
        self.Locator = locator

    def Search(self, lat, lng, radiusMeters, selectedTags, itemCount):
        if(selectedTags!=None):
            #Changing tags to lower case to enable a virtual case-insensitive comparison. Note that this does not work for all cultures
            selectedTags = set([tag.lower() for tag in selectedTags])
        else:
            selectedTags = set()

        #Get elements within the search radius
        filteredResults = self.Locator.Search(lat,lng,radiusMeters)

        #If any tags were selected, filter elements which do not share at least one tag with selectedTags
        if len(selectedTags)>0:
            filteredResults = [shopLocation for shopLocation in filteredResults if not shopLocation.Shop.tags.isdisjoint(selectedTags)]

        #Get top N most popular products of shops
        results = SortedListWithKey(key=lambda val: -1*float(val.Product.popularity))
        for item in filteredResults:
            #results = results[0:itemCount] #might be useful if concerns related to memory take precedence over processing time
            
            #Get most popular products of this shop
            topProducts = item.Shop.products[0:itemCount]

            for product in topProducts:
                #Check at which position this element would be if inserted into the aggregated popular products list
                index = results.bisect_right(ShopProduct(item.Shop,product))
                if index < itemCount:
                    #The product is higher in popularity than the current threshold 
                    results.add(ShopProduct(item.Shop,product))
                else:
                    #The aggregated list already contains enough number of products which are more popular than the one being considered
                    break
        results = results[0:itemCount]

        #results is a SortedListWithKey consisting of ShopProduct objects

        return results