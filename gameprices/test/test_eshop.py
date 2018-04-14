import unittest
import sys
from gameprices.shops.eshop import Eshop
from gameprices.cli.cli import eshop_main
import pytest

from gameprices.cli.mailalert import main as psnmailalert_main
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


    def test_mailfunc(self):
        mailalert(
            "DE/de###1174779###Sonic_Mania,100.00,DE/de", psnmailalert_main)
