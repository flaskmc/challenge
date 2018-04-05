class Location(object):
    """ An entity which holds Latitude and Longitude information """
    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

    @property
    def Latitude(self):
        return self._latitude

    @Latitude.setter
    def Latitude(self, value):
        self._latitude = value

    @property
    def Longitude(self):
        return self._longitude

    @Longitude.setter
    def Longitude(self, value):
        self._longitude = value


