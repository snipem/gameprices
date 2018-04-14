from psnprices.offer import GameOffer


class Shop(object):
    """A generic videm game shop"""

    def __init__(self, country):
        super(Shop, self).__init__()
        self.country = country

    def get_item_by(self, id, name):
        game_offers = self.search(name)
        for game_offer in game_offers:
            if game_offer.id == id:
                return game_offer
