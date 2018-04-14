from gameprices.offer import GameOffer


class Shop(object):
    """A generic videm game shop"""

    def __init__(self, country):
        super(Shop, self).__init__()
        self.country = country
