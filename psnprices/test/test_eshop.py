import unittest
import sys
from psnprices.shops.eshop import Eshop
from psnprices.cli.psncli import eshop_main

class EshopTest(unittest.TestCase):

    eshop = Eshop(country="DE/de")

    def test_getItemForId(self):
        game_offers = self.eshop.search("Celeste")
        game_offer = game_offers[0]
        assert game_offer.name == "Celeste"

    def test_search_alot(self):
        game_offers = self.eshop.search("a")
        print('\n'.join(str(e) for e in game_offers))
        assert len(game_offers) > 1

    def test_get_item_by_id(self):
        id = "1207064"
        name = "Celeste"
        game_offer = self.eshop.get_item_by(id=id, name=name)

        assert game_offer.name == name
        assert game_offer.id == id 

    def test_cli(self):
        sys.argv = [
            "eshopcli",
            "--query",
            "'Vostok'"
            ]
        eshop_main()
