import unittest
import sys
from psnprices.shops.eshop import Eshop
from psnprices.cli.psncli import eshop_main
import pytest

from psnprices.cli.psnmailalert import main as psnmailalert_main
from . commons import mailalert


class EshopTest(unittest.TestCase):

    eshop = Eshop(country="DE")

    def test_get_item_for_id(self):
        game_offers = self.eshop.search("Celeste")
        game_offer = game_offers[0]
        assert game_offer.name == "Celeste"

    def test_search_alot(self):
        game_offers = self.eshop.search("a")
        print('\n'.join(str(e) for e in game_offers))
        assert len(game_offers) > 1

    def test_id_encoder(self):
        assert "DE###1207064###Celeste_123" == self.eshop._encode_id(
            id=1207064, name="Celeste 123")

    def test_id_decoder(self):
        assert ("DE", "1207064", "Celeste 123") == self.eshop._decode_id(
            "DE###1207064###Celeste_123")

    def test_cli(self):
        sys.argv = [
            "eshopcli",
            "--query",
            "'Vostok'"
        ]

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            eshop_main()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0

    def test_mailfunc(self):
        mailalert(
            "DE/de###1174779###Sonic_Mania,100.00,DE/de", psnmailalert_main)
