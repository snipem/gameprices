#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from gameprices.shops import psn
from gameprices.shops.psn import Psn

from gameprices.cli.mailalert import main as psnmailalert_main
from . commons import mailalert

class PsnTest(unittest.TestCase):

    # CID for item that is free for Plus members but not for normal members
    # TuneIt on german store
    freeForPlusCid = "EP4423-PCSB00407_00-TUNEIN0000000000"
    psn = Psn(country="DE/de")


    def test_search_for_cid_by_title_in_german_store(self):
        cids = psn._get_cid_for_name("Metal Gear", "DE/de")

        assert len(cids) > 0

    def test_search_for_cid_by_title_in_us_store(self):
        cids = psn._get_cid_for_name("Metal Gear", "US/en")

        assert len(cids) > 0

    def test_get_item_for_cid(self):
        store = "DE/de"
        cids = psn._get_cid_for_name("Tearaway", store)
        item = psn._getItemForCid(cids[0], store)

        assert item['name'] is not None

    def test_get_item_for_cid2(self):
        store = "DE/de"
        cids = psn._get_cid_for_name("Child of Light", store)
        item = psn._getItemForCid(cids[0], store)

        assert item['name'] is not None

    def test_get_item_by_container(self):
        store = "DE/de"
        items = psn._get_items_by_container(
            'STORE-MSF75508-PLUSINSTANTGAME', store, {"platform": "ps4"})

        assert len(items) > 0

    def test_get_playstation_plus_price(self):
        store = "DE/de"
        item = psn._getItemForCid(self.freeForPlusCid, store)

        print(
            "Using '" +
            item['name'] +
            "' (" +
            self.freeForPlusCid +
            ") from " +
            store +
            " for comparison. Item must be free for Plus members in order to pass the unit test. This might fail due to price changes")

        assert item is not None

        normalPrice = psn._get_price(item)
        plusPrice = psn._get_playstation_plus_price(item)

        print ("Normal Price: ", "%.2f" %
               normalPrice, "Plus Price: ", "%.2f" % plusPrice)

        assert isinstance(normalPrice, float)
        assert isinstance(plusPrice, float)
        assert plusPrice == 0

    def test_check_currency_symbolAsPartOfName(self):
        store = "DE/de"
        cids = psn._get_cid_for_name("Child of Light", store)
        item = psn._getItemForCid(cids[0], store)
        assert psn._get_display_price(item, store)[0] == u'\N{EURO SIGN}'

    def test_check_currency_symbol(self):
        assert psn._get_currency_symbol("DE/de") == u'\N{EURO SIGN}'
        assert psn._get_currency_symbol("US/en") == u'\N{DOLLAR SIGN}'
        assert psn._get_currency_symbol("JP/jp") == u'\N{YEN SIGN}'
        assert psn._get_currency_symbol("Unknown") == ''

    def test_get_rewards(self):
        store = "DE/de"
        item = psn._getItemForCid(
            "EP0006-CUSA02532_00-UNRAVELUNRAVEL09", store)
        assert len(psn._get_rewards(item)) > -1

    @unittest.skip("Skip temporary price reduction")
    def test_check_currently_reduced_item_all_prices(self):
        store = "DE/de"
        item = psn._getItemForCid(
            "EP2107-CUSA00327_00-DONTSTARVEPS4V01", store)
        print("Checking: ", item['name'])
        assert psn._get_normal_price(item) == 13.99
        assert psn._get_playstation_plus_price(item) == 4.89
        assert psn._get_non_playstation_plus_price(item) == 6.99
        assert psn._get_price(item) == 4.89

    @unittest.skip("Skip temporary price reduction")
    def test_check_currently_reduced_item_no_plus_reduction(self):
        store = "DE/de"
        item = psn._getItemForCid(
            "EP9000-CUSA00194_00-UNTILDAWN0000001", store)
        print("Checking: ", item['name'])
        assert psn._get_normal_price(item) == 59.99
        assert psn._get_playstation_plus_price(item) is None
        assert psn._get_non_playstation_plus_price(item) == 44.99
        assert psn._get_price(item) == 44.99

    def test_determine_storeFromCID(self):
        assert psn._determine_store(
            "EP9000-CUSA00194_00-UNTILDAWN0000001") == "DE/de"
        assert psn._determine_store(
            "JP0006-NPJB00377_00-BATTLEFIELD40000") == "JP/jp"
        assert psn._determine_store(
            "UP2034-CUSA04841_00-NMSDIGITAL000001") == "US/en"
        assert psn._determine_store("1") is None

    def get_game(
            self,
            name="Bloodborne",
            id="EP9000-CUSA00207_00-BLOODBORNE0000EU"):
        game = self.psn.get_item_by(name=name, id=id)
        return game

    def test_get_item_for_id(self):
        game_offers = self.psn.search("Tearaway™ Unfolded")
        game_offer = game_offers[0]
        assert game_offer.name == "Tearaway™ Unfolded"

    def test_search_alot(self):
        game_offers = self.psn.search("park")
        print('\n'.join(str(e) for e in game_offers))
        assert len(game_offers) > 1

    def test_search_test_without_playable_platforms(self):
        game_offers = self.psn.search("test")
        print('\n'.join(str(e) for e in game_offers))
        assert len(game_offers) > 1

    def test_get_item_by_id(self):
        id = "EP9000-CUSA00562_00-TEARAWAYUNFOLDED"
        name = "Tearaway™ Unfolded"
        game_offer = self.psn.get_item_by(id=id, name=name)

        assert game_offer.name == name
        assert game_offer.id == id

    def test_game_has_picture(self):
        assert "http" in self.get_game().picture_url

    def test_mailfunc(self):
        mailalert(
            "EP0177-CUSA07010_00-SONICMANIA000000,100.00", psnmailalert_main)
