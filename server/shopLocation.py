from location import Location

class ShopLocation(object):
    """ A composite entity which holds a Shop and its corresponding Location """

    def __init__(self, shop, location):
        self._location = location
        self._shop = shop

    @property
    def Location(self):
        return self._location

    @Location.setter
    def Location(self, value):
        self._location = value

    @property
    def Shop(self):
        return self._shop

    @Shop.setter
    def Shop(self, value):
        self._shop = value