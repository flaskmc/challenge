class ShopProduct(object):
    """ A composite entity which holds a Product and its corresponding Shop """
    def __init__(self, shop, product):
        self._product = product
        self._shop = shop

    @property
    def Product(self):
        return self._product

    @Product.setter
    def Product(self, value):
        self._product = value

    @property
    def Shop(self):
        return self._shop

    @Shop.setter
    def Shop(self, value):
        self._shop = value