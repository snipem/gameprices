class GameOffer(object):
    """docstring for ClassName."""

    id = None
    name = None
    prices = []
    platforms = []
    picture_url = None

    def __init__(self, id, picture_url, name, url, prices, platforms):
        super(GameOffer, self).__init__()
        self.prices = prices
        self.name = name
        self.id = id
        self.url = url
        self.picture_url = picture_url
        self.platforms = platforms

    def __str__(self):
        return "%s - %s on %s" %(self.name, self.prices, self.platforms)

    def get_item_by(self, id, name):
        raise NotImplementedError

    def search(self, name):
        raise NotImplementedError

class Price(object):
    def __init__(self, value, currency, offer_type):
        super(Price, self).__init__()
        self.value = value
        self.currency = currency
        self.offer_type = offer_type


            