from decimal import Decimal
import geopy
from geopy.distance import VincentyDistance
from location import Location

class CoordinateHelper(object):
    """ A helper class which provides helper methods for location based operations"""
    @staticmethod
    def CastString2Coordinates(lat, lng):
        """ Returns a Location object from given string parameters. """
        try:
            _lat=Decimal(lat.strip())
            _lng=Decimal(lng.strip())

            if (_lat > 90 or _lat < -90) or (_lng > 180 or _lng < -180):
                return None
            else:
                return Location(_lat, _lng)
        except ValueError:
            return None
    
    @staticmethod
    def GetDistanceMeters(location1, location2):
        """ Calculates the distance between points represented by two Location objects """
        p1 = (location1.Latitude, location1.Longitude)
        p2 = (location2.Latitude, location2.Longitude)
        result = VincentyDistance(p1, p2).meters
        return result

    @staticmethod
    def GetDistanceMetersFromLatLng(lat1, lng1, lat2, lng2):
        """ Calculates the distance between points represented by given parameters """
        p1 = (lat1, lng1)
        p2 = (lat2, lng2)
        result = VincentyDistance(p1, p2).meters
        return result