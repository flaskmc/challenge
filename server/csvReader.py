import csv
from entity import Entity

class CsvReader:
    """ A class which provides functionality for loading csv files into a set of entities/models """
    def Read(self, file, initializer=None):
        """ Loads a csv file into a dictionary of entities/models. Values in the first column are used as keys. """
        data = list(csv.reader(open(file)))
        if initializer is None:
            instances = dict( [ (i[0], Entity(i, data[0])) for i in data[1:]] )
        else:
            instances = dict( [ (i[0], initializer(Entity(i, data[0]))) for i in data[1:]] )
        return instances

    def ReadList(self, file, initializer=None):
        """ Loads a csv file into a dictionary of entities/models. """
        data = list(csv.reader(open(file)))
        if initializer is None:
            instances = [Entity(i, data[0]) for i in data[1:]]
        else:
            instances = [initializer(Entity(i, data[0])) for i in data[1:]]
        return instances