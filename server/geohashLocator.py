from alocator import ALocator
from pytrie import StringTrie
from location import Location
from coordinateHelper import CoordinateHelper
import Geohash
import proximityhash

class GeohashLocator(ALocator):
    """ A class which can be used to locate points within specified radius of a center
        This particular type of Locator uses geohashing for fast searches.
        However, results usually also include locations which are slightly more distant than desired.
        Consider using HybridLocator which runs a search with GeohashLocator and further filters the initial larger set of results with a more precise distance based BasicLocator.
        In addition, geohash values of close locations differ significantly around polar and equatorial regions as well as prime meridian and +-180 meridians.
        Consider using HybridLocator which falls back to using BasicLocator when a search is being conducted around the specified regions.
    """
    def __init__(self, itemCollection):
        if itemCollection == None:
            raise ValueError()
        self.container = GeohashContainer(itemCollection)
        #self.base32 = ['0','1','2','3','4','5','6','7','8','9','b','c','d','e','f','g','h','j','k','m','n','p','q','r','s','t','u','v','w','x','y','z']

    def Search(self, lat, lng, radiusMeters):
        """ Returns locations which are within the specified distance of the location. """
        if abs(lat)>90 or abs(lng)>180 or radiusMeters<=0:
            raise ValueError
        #radius is increased by 10% so that hashes are created for a larger area. Ultimately this does not end in out of range results since there is a final filtering step
        #create_geohash method returns a set of geohash values which represent the specified area (usually, resulting geohashes represent a sligthtly larger area)
        proximityHashString = proximityhash.create_geohash(lat, lng, radiusMeters*1.1, 7, True)
        hashes = proximityHashString.split(",")
        
        results=[]
        for geohash in hashes:
            results.extend(self.container.Retrieve(geohash))
        
        return results

    def Add(self, key, value):
        self.container.Add(key, value)

class GeohashContainer(object):
    """ A class which can be used as a container of geohashes and corresponding items. The underlying data structure is a trie (StringTrie)."""
    def __init__(self, itemCollection):
        self.container = StringTrie()
        for item in itemCollection:
            self.container[Geohash.encode(item.Location.Latitude, item.Location.Longitude)] = item

    def Retrieve(self, keyPrefix):
        """ Returns all items which match the specified keyPrefix """
        results = self.container.values(keyPrefix)
        return results

    def Add(self, key, value):
        """ Adds a new item to its underlying container """
        self.container[key] = value