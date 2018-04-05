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
        
        #changing tags to lower case to enable a virtual case-insensitive comparison. Note that this does not work for all cultures
        selectedTags = set([tag.lower() for tag in selectedTags])

        #get elements within the search radius
        filteredResults = self.Locator.Search(lat,lng,radiusMeters)

        if len(selectedTags)>0:
            filteredResults = [ShopLocation(shop,location) for location, shop in filteredResults if not shop.tags.isdisjoint(selectedTags)]

        print('tagfilter complete')
        print(len(filteredResults))
        allresults = SortedListWithKey(key=lambda val: -1*float(val.Product.popularity))
        results = SortedListWithKey(key=lambda val: -1*float(val.Product.popularity))
        for item in filteredResults:
            
            topProducts = item.Shop.products[0:itemCount]
            print('top product count')
            print(len(topProducts))
            for product in topProducts:
                index = results.bisect_right(ShopProduct(item.Shop,product))
                allresults.add(ShopProduct(item.Shop,product))
                if index < itemCount:
                    results.add(ShopProduct(item.Shop,product))
                else:
                    break
        results = results[0:itemCount]

        print('itemCcount filter complete')
        print(len(results))

        for result in results:
            print(result.Product.popularity, result.Shop.name)

        print("=========")
        #for result in allresults:
            #print(result.Product.popularity, result.Shop.name)

        #results is a SortedListWithKey consisting of (product, shop) tuples

        return results