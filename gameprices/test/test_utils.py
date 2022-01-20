from unittest import TestCase

from gameprices.offer import GameOffer
from gameprices.price import Price
from gameprices.utils.utils import format_items_as_text


class Test(TestCase):
    def test_format_items_as_text(self):
        prices = []

        prices.append(Price(
            value=20.0,
            offer_type="NORMAL",
        ))

        prices.append(Price(
            value=10.5,
            offer_type="PS+",
        ))

        game_offer = GameOffer(
            id="id",
            cid="cid",
            url="url",
            type="FULL_GAME",
            name="NAME",
            prices=prices,
            platforms=["PS4", "PS Vita"],
            picture_url="http://picture.jpg",
        )

        formatted_items = format_items_as_text([game_offer])
        self.assertEqual("cid\tNAME\tPS4,PS Vita\t10.50\tFULL_GAME", formatted_items[0])
