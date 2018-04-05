class Entity: 
    """ An entity class which gets initialized from csv inputs """
    def __init__(self, row, header):
        self.__dict__ = dict(zip(header, row))