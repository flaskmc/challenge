from geohashLocator import GeohashLocator
from basicLocator import BasicLocator
from hybridLocator import HybridLocator
from dataLoader import CsvDataLoader

#This is not a desirable method of dependency injection, consider using DI frameworks
class LocatorInitializer(object):
    """ A class for initializing Locator objects """
    #This is not a desirable method of dependency injection, consider using DI frameworks
    def Initialize(self, shopsPath, tagsPath, taggingsPath, productsPath):
        dataLoader = CsvDataLoader()
        shopLocationCollection = dataLoader.Load(shopsPath, tagsPath, taggingsPath, productsPath)
        return HybridLocator(GeohashLocator(shopLocationCollection), BasicLocator(shopLocationCollection))