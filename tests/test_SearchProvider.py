from server.basicLocator import BasicLocator
from server.geohashLocator import GeohashLocator
from server.hybridLocator import HybridLocator
from server.location import Location
from server.shopLocation import ShopLocation
from server.entity import Entity
from server.coordinateHelper import CoordinateHelper
from server.searchProvider import SearchProvider
from sortedcontainers import SortedListWithKey
import unittest

class TestSearchProvider(unittest.TestCase):
    def setUp(self):
        self.shopLocations = self.InitLocationCollection(10)
        self.origin = Location(59.3325800, 18.0649000)

    def InitLocationCollection(self, count, latOrigin=59.3325800, lngOrigin=18.0649000, latIncrement = 0.001, lngIncrement = 0.001):
        shopLocations=[]
        shops = self.InitShops(count)
        #init regular locations
        for i in range(0, count):
            lat = latOrigin + i*latIncrement
            lng = lngOrigin + i*lngIncrement
            location = Location(lat, lng)
            shopLocations.append(ShopLocation(shops[i], location))

        return shopLocations
    
    def InitShops(self, count):
        shops = []
        for i in range(0,count):
            shop = Entity(["id","name","lat","lng"],["id","name","lat","lng"])
            product = Entity(["id","shop_id","title",str(i),"1"],["id","shop_id","title","popularity","quantity"])
            shop.products = SortedListWithKey(key=lambda val: -1*float(val.popularity))
            shop.products.add(product)
            if i%2 == 0:
                shop.tags = set(["tag1","tag2"])
            else:
                shop.tags = set(["taga","tagb"])
            shops.append(shop)
        return shops

    def test_search_returns_results_when_tags_empty(self):
        #Todo: use mocking for supplying objects
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = GeohashLocator(self.shopLocations)
        locator = HybridLocator(geohashLocator, basicLocator) 
        provider = SearchProvider(locator)
        radius = 1000
        
        searchResults = provider.Search(self.origin.Latitude, self.origin.Longitude, radius, set(), 10)

        resultCount = len(searchResults)
        self.assertGreater(resultCount, 0)

    def test_search_returns_results_when_tags_null(self):
        #Todo: use mocking for supplying objects
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = GeohashLocator(self.shopLocations)
        locator = HybridLocator(geohashLocator, basicLocator) 
        provider = SearchProvider(locator)
        radius = 1000
        
        searchResults = provider.Search(self.origin.Latitude, self.origin.Longitude, radius, None, 10)

        resultCount = len(searchResults)
        self.assertGreater(resultCount, 0)

    def test_search_returns_only_results_with_specified_tags(self):
        #Todo: use mocking for supplying objects
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = GeohashLocator(self.shopLocations)
        locator = HybridLocator(geohashLocator, basicLocator) 
        provider = SearchProvider(locator)
        radius = 1000
        
        tags = ["tag1", "---"]
        searchResults = provider.Search(self.origin.Latitude, self.origin.Longitude, radius, set(tags), 10)

        resultCount = len(searchResults)
        self.assertGreater(resultCount, 0)

        for element in searchResults:
            self.assertTrue(tags[0] in element.Shop.tags)

    def test_search_returns_empty_when_no_matching_tags(self):
        #Todo: use mocking for supplying objects
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = GeohashLocator(self.shopLocations)
        locator = HybridLocator(geohashLocator, basicLocator) 
        provider = SearchProvider(locator)
        radius = 1000
        
        tags = ["---"]
        searchResults = provider.Search(self.origin.Latitude, self.origin.Longitude, radius, set(tags), 10)

        resultCount = len(searchResults)
        self.assertEqual(resultCount, 0)

    def test_search_returns_empty_when_maximumItemCount_is_zero(self):
        #Todo: use mocking for supplying objects
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = GeohashLocator(self.shopLocations)
        locator = HybridLocator(geohashLocator, basicLocator) 
        provider = SearchProvider(locator)
        radius = 1000
        
        
        searchResults = provider.Search(self.origin.Latitude, self.origin.Longitude, radius, None, 0)

        resultCount = len(searchResults)
        self.assertEqual(resultCount, 0)

    def test_search_returns_empty_when_maximumItemCount_is_negative(self):
        #Todo: use mocking for supplying objects
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = GeohashLocator(self.shopLocations)
        locator = HybridLocator(geohashLocator, basicLocator) 
        provider = SearchProvider(locator)
        radius = 1000
        
        
        searchResults = provider.Search(self.origin.Latitude, self.origin.Longitude, radius, None, -1)

        resultCount = len(searchResults)
        self.assertEqual(resultCount, 0)

    def test_search_returns_requested_count_of_results(self):
        #Todo: use mocking for supplying objects
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = GeohashLocator(self.shopLocations)
        locator = HybridLocator(geohashLocator, basicLocator) 
        provider = SearchProvider(locator)
        radius = 1000
        
        count = 5
        searchResults = provider.Search(self.origin.Latitude, self.origin.Longitude, radius, None, count)

        resultCount = len(searchResults)
        self.assertEqual(resultCount, count)


    def test_search_returns_all_elements_when_requested_count_is_more_than_element_count(self):
        #Todo: use mocking for supplying objects
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = GeohashLocator(self.shopLocations)
        locator = HybridLocator(geohashLocator, basicLocator) 
        provider = SearchProvider(locator)
        radius = 5000
        
        count = 50000
        searchResults = provider.Search(self.origin.Latitude, self.origin.Longitude, radius, None, count)

        totalCount = len(self.shopLocations)
        resultCount = len(searchResults)
        self.assertEqual(resultCount, totalCount)
