from gameprices.offer import GameOffer


class Shop(object):
    """A generic video game online store"""

    def __init__(self, country):
        super(Shop, self).__init__()
        self.country = country

    def search(self, name):
        super(Shop, self).search()
