from alocator import ALocator
from location import Location
from coordinateHelper import CoordinateHelper

class BasicLocator(ALocator):
    """ A class which can be used to locate points within specified radius of a center
        This particular type of Locator checks the distance between each known location and the center and returns the ones which are within the radius.
        This method provides precise results but can get computationally expensive when the total collection of candidate locations is of a considerable size
        Consider using HybridLocator which runs a search with GeohashLocator and further filters the initial larger set of results with a more precise distance based BasicLocator.
    """
    def __init__(self, locationCollection):
        if locationCollection == None:
            raise ValueError()
        self.container = locationCollection
        
    def Search(self, lat, lng, radiusMeters):
        """ Returns items within the provided radius. The operation is performed on object's container. """
        if abs(lat)>90 or abs(lng)>180 or radiusMeters<=0:
            raise ValueError
        loc1 = Location(lat, lng)

        results=[]
        for item in self.container:
            if CoordinateHelper.GetDistanceMeters(loc1, item.Location) <= radiusMeters:
                results.append(item)

        return results

    
    def SearchInIterable(self, lat, lng, radiusMeters, iterable):
        """ Returns items within the provided radius. The operation is performed on the provided iterable. """
        if abs(lat)>90 or abs(lng)>180 or radiusMeters<=0:
            raise ValueError
        
        loc1 = Location(lat, lng)

        results=[]
        for item in iterable:
            if CoordinateHelper.GetDistanceMeters(loc1, item.Location) <= radiusMeters:
                results.append(item)

        return results

    def SearchInIterableWithLocationSelector(self, lat, lng, radiusMeters, iterable, locationSelector):
        """ Returns items within the provided radius. The operation is performed on the provided iterable. The object referenced by locationSelector parameter is used for selecting the Location from iterable's items. """
        loc1 = Location(lat, lng)

        results=[]
        for item in iterable:
            if CoordinateHelper.GetDistanceMeters(loc1, locationSelector(item)) <= radiusMeters:
                results.append(item)

        #[item for item in iterable if CoordinateHelper.GetDistanceMeters(loc1, locationSelector(item)) <= radiusMeters]

        return results