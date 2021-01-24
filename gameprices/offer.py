import json


class GameOffer(object):
    """docstring for ClassName."""

    id = None
    name = None
    prices = []
    platforms = []
    picture_url = None

    def __init__(
            self,
            id,
            cid,
            name,
            url,
            prices,
            platforms,
            picture_url=None,
            type=None):
        super(GameOffer, self).__init__()
        self.prices = prices
        self.name = name
        self.id = id
        self.cid = cid
        self.url = url
        self.type = type
        # TODO
        self.picture_base_url = "TODO"
        self.picture_url = picture_url
        self.platforms = platforms

    def __str__(self):
        return "%s - %s on %s" % (self.name, self.prices,
                                  ",".join(self.platforms))

    def dump(self):
        return {'id': self.id,
                'name': self.name,
                'type': self.type,
                'prices': [o.dump() for o in self.prices], # TODO Don't print null values
                'platforms': self.platforms}

    def get_item_by(self, id, name):
        raise NotImplementedError

    def search(self, name):
        raise NotImplementedError

    def get_full_image(self):
        return self.picture_base_url + self.picture_url


class Price(object):

    def __init__(self, value, currency, offer_type):
        super(Price, self).__init__()
        self.value = value
        self.currency = currency
        self.offer_type = offer_type

    def dump(self):
        return {
            'price': self.value,
            'currency': self.currency,
            'type': self.offer_type,
        }
