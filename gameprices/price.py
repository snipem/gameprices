class Price(object):
    def __init__(self, value, offer_type):
        super(Price, self).__init__()
        self.value = value
        self.offer_type = offer_type

    def dump(self):
        return {
            "price": self.value,
            "type": self.offer_type,
        }
