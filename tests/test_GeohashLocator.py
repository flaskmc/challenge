from server.geohashLocator import GeohashLocator
from server.location import Location
from server.shopLocation import ShopLocation
from server.coordinateHelper import CoordinateHelper
import unittest

class TestGeohashLocator(unittest.TestCase):
    def setUp(self):
        self.shopLocations = self.InitLocationCollection(10)
        self.origin = Location(59.3325800, 18.0649000)

    def InitLocationCollection(self, count, latOrigin=59.3325800, lngOrigin=18.0649000, latIncrement = 0.001, lngIncrement = 0.001):
        shopLocations=[]
        for i in range(0, count):
            lat = latOrigin + i*latIncrement
            lng = lngOrigin + i*lngIncrement
            location = Location(lat, lng)
            shopLocations.append(ShopLocation(None, location))
        return shopLocations
        
    def test_results_contain_all_items_within_range(self):

        locator = GeohashLocator(self.shopLocations)
        radius = 1000

        geohashSearchResults = locator.Search(self.origin.Latitude, self.origin.Longitude, radius)
        hashSearchResultCount = len(geohashSearchResults)
        self.assertGreater(hashSearchResultCount, 0)

        bruteforceResults = []
        for item in self.shopLocations:
            distance = CoordinateHelper.GetDistanceMeters(self.origin, item.Location)
            if distance <= radius:
                bruteforceResults.append(item)
        bruteforceResultCount = len(bruteforceResults)

        self.assertGreaterEqual(hashSearchResultCount, bruteforceResultCount)
        
        self.assertTrue(set(bruteforceResults).issubset(set(geohashSearchResults)))

    def test_result_contains_known_location(self):
        locator = GeohashLocator(self.shopLocations)
        radius = 10 #use a small radius to get as few as possible

        searchResults = locator.Search(self.origin.Latitude, self.origin.Longitude, radius)
        self.assertGreater(len(searchResults), 0)

        contains=False
        for item in searchResults:
            if (item.Location.Latitude == self.origin.Latitude) and (item.Location.Longitude == self.origin.Longitude):
                contains = True
                break

        self.assertTrue(contains)

    def test_results_are_not_empty(self):
        locator = GeohashLocator(self.shopLocations)
        radius = 1000

        searchResults = locator.Search(self.origin.Latitude, self.origin.Longitude, radius)

        self.assertGreater(len(searchResults), 0)
    
    def test_results_are_empty_when_none_in_range(self):
        locator = GeohashLocator(self.shopLocations)
        radius = 1000

        searchResults = locator.Search(self.origin.Latitude + 5, self.origin.Longitude + 5, radius)

        self.assertEqual(len(searchResults), 0)

    def test_search_raises_when_radius_negative(self):
        locator = GeohashLocator(self.shopLocations)
        radius = -1

        with self.assertRaises(ValueError):
            locator.Search(self.origin.Latitude, self.origin.Longitude, radius)

    def test_constructor_raises_when_container_is_null(self):
        
        
        with self.assertRaises(ValueError):
            GeohashLocator(None)
    
    def test_search_raises_when_negative_coordinates(self):
        locator = GeohashLocator(self.shopLocations)
        radius = 1000
        
        with self.assertRaises(ValueError):
            locator.Search(-1000, -1000, radius)
            