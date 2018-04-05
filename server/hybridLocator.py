from alocator import ALocator

class HybridLocator(ALocator):
    """ A class which can be used to locate points within specified radius of a center
        This particular type of Locator uses both GeohashLocator and BasicLocator in order to achieve fast and accurate results.
        In order to avoid geohashing limitations HybridLocator falls back to using BasicLocator when a search is being conducted around polar and equatorial regions as well as prime meridian and +-180 meridians.
    """
    def __init__(self, geohashLocator, basicLocator):
        self.geohashLocator = geohashLocator
        self.basicLocator = basicLocator
        
    def Search(self, lat, lng, radiusMeters):
        """ Returns locations which are within the specified distance of the location. """

        #Around the boundary locations, Geohashing produces quite different hashes for points close to eachother.
        #This is a coarse way of dealing with limitations of geohashing around polar and equatorial regions as well as prime meridian and +-180 meridians
        #A better aproach could be setting search origin's longitude to 0 and checking whether it is closer than the radius. Then apply the same principle to other edge lats and lngs to see if the circle of interest intersects with those
        if ((lat < 89 and lat > 1) or (lat < -1 and lat > -89)) and ((lng < 179 and lng > 1) or (lng < -1 and lng > -179)):
            geohashResults = self.geohashLocator.Search(lat, lng, radiusMeters)
            #geohashResuls contains a list of (Location, shop) tuples.
            #Geohash result collection is likely to include some extra items, so we make a final check on the result collection
            return self.basicLocator.SearchInIterable(lat,lng,radiusMeters,geohashResults)
        else:
            return self.basicLocator.Search(lat, lng, radiusMeters)