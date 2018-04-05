from csvReader import CsvReader
from extenders import Extenders
from coordinateHelper import CoordinateHelper
from shopLocation import ShopLocation

class CsvDataLoader(object):
    """ A class which is used to load csv files into a set of entities and make object level associations between individual entities"""
    def Load(self, shopsPath, tagsPath, taggingsPath, productsPath):
        """ Loads provided csv files into entities. Returns a list of ShopLocation objects """
        
        reader = CsvReader()
        #read files into entity collections
        shops = reader.Read(shopsPath, Extenders.InitializeExtendedShop)
        tags = reader.Read(tagsPath)
        taggings = reader.ReadList(taggingsPath)
        products = reader.ReadList(productsPath)

        #match shops with tags
        for tagging in taggings:
            try:
                #tags are added in lowercase for case insensitive comparison. Lowercase comparison does not work for all cultures, consider using another method
                shops[tagging.shop_id].tags.add(tags[tagging.tag_id].tag.lower())
            except KeyError:
                continue
        #match shops with products
        for product in products:
            try:
                shops[product.shop_id].products.add(product)
            except KeyError:
                continue
        
        #build a list of ShopLocation objects to represent final results
        shopLocationCollection = []
        for i, shop in shops.iteritems():
            coordinates = CoordinateHelper.CastString2Coordinates(shop.lat, shop.lng)

            if (coordinates==None):
                continue
            else:
                shopLocationCollection.append(ShopLocation(shop,coordinates))
        
        #return a list of ShopLocation objects
        return shopLocationCollection
