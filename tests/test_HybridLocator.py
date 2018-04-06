from server.basicLocator import BasicLocator
from server.geohashLocator import GeohashLocator
from server.hybridLocator import HybridLocator
from server.location import Location
from server.shopLocation import ShopLocation
from server.coordinateHelper import CoordinateHelper
import unittest

class TestHybridLocator(unittest.TestCase):
    def setUp(self):
        self.shopLocations = self.InitLocationCollection(10)
        self.origin = Location(59.3325800, 18.0649000)

    def InitLocationCollection(self, count, latOrigin=59.3325800, lngOrigin=18.0649000, latIncrement = 0.001, lngIncrement = 0.001):
        shopLocations=[]
        #init regular locations
        for i in range(0, count):
            lat = latOrigin + i*latIncrement
            lng = lngOrigin + i*lngIncrement
            location = Location(lat, lng)
            shopLocations.append(ShopLocation(None, location))
        #init locations close to equator, poles and prime meridian
        equator = ShopLocation(None, Location(0,lngOrigin))
        pole1 = ShopLocation(None, Location(89.5,lngOrigin))
        pole2 = ShopLocation(None, Location(-89.5,lngOrigin))
        primeMeridian = ShopLocation(None, Location(latOrigin,0))
        edgeMeridian1 = ShopLocation(None, Location(latOrigin,179.5))
        edgeMeridian2 = ShopLocation(None, Location(latOrigin,-179.5))
        shopLocations.extend([equator,pole1,pole2,primeMeridian,edgeMeridian1,edgeMeridian2])

        return shopLocations
        

    def test_only_basicLocator_used_when_searching_close_to_primemeridian(self):
        #Todo: use mocking for supplying objects and testing method calls. For now just uses an exception for telling if a member was accessed
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = None
        locator = HybridLocator(geohashLocator, basicLocator) 
        radius = 1000

        #call will throw an exception if geohashLocator is used
        locator.Search(0, 0, radius)

    def test_geohashLocator_used_when_searching_in_non_edge_location(self):
        #Todo: use mocking for supplying objects and testing method calls. For now just uses an exception for telling if a member was accessed
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = None
        locator = HybridLocator(geohashLocator, basicLocator) 
        radius = 1000

        with self.assertRaises(AttributeError):
            #call will throw an exception if geohashLocator is used
            locator.Search(self.origin.Latitude, self.origin.Longitude, radius)
        

    def test_search_returns_known_item_when_location_is_edge(self):
        #Todo: use mocking for supplying objects and testing method calls.
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = None
        locator = HybridLocator(geohashLocator, basicLocator) 
        radius = 1000

        #call will throw an exception if geohashLocator is used
        searchResults = locator.Search(self.origin.Latitude, 0, radius)

        resultCount = len(searchResults)
        self.assertEqual(resultCount, 1)

        item = searchResults[0]
        self.assertEqual(item.Location.Latitude,self.origin.Latitude)
        self.assertEqual(item.Location.Longitude,0)

        #Continue testing other edge locations

    def test_search_returns_known_item_when_location_is_not_edge(self):
        #Todo: use mocking for supplying objects and testing method calls.
        basicLocator = BasicLocator(self.shopLocations)
        geohashLocator = GeohashLocator(self.shopLocations)
        locator = HybridLocator(geohashLocator, basicLocator) 
        radius = 1000

        searchResults = locator.Search(self.origin.Latitude, self.origin.Longitude, radius)

        resultCount = len(searchResults)
        self.assertGreater(resultCount, 0)

        contains=False
        for item in searchResults:
            if (item.Location.Latitude == self.origin.Latitude) and (item.Location.Longitude == self.origin.Longitude):
                contains = True
                break

        self.assertTrue(contains)

    