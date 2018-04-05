from abc import ABCMeta, abstractmethod

#Abstract class defining a locator members
class ALocator:
    """ An abstract class which specifies the contract for locating points within specified radius of a center """
    __metaclass__ = ABCMeta
    @abstractmethod
    def Search(self, lat, lng, radiusMeters):
        pass