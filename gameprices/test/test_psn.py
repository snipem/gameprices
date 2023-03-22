#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import pytest

from gameprices.shops import psn
from gameprices.shops.psn import Psn
from gameprices.cli import *

from gameprices.cli.mailalert import main as psnmailalert_main
from gameprices.test.commons import mailalert
from gameprices.utils.utils import format_items_as_json

NO_SEARCH_FOR_CID_REASON = "The search for IDs with the new PSN API as of 2020 is not yet implemented"

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

    @pytest.mark.skip(reason=NO_SEARCH_FOR_CID_REASON)
    def test_get_item_for_cid(self):
        store = "DE/de"
        cids = psn._get_cid_for_name("Tearaway", store)
        item = psn._get_item_for_cid(cids[0], store)

        assert item["name"] is not None

    @pytest.mark.skip(reason=NO_SEARCH_FOR_CID_REASON)
    def test_get_item_for_cid2(self):
        store = "DE/de"
        cids = psn._get_cid_for_name("Child of Light", store)
        item = psn._get_item_for_cid(cids[0], store)

        assert item["name"] is not None

    @pytest.mark.skip(reason=NO_SEARCH_FOR_CID_REASON)
    def test_get_playstation_plus_price(self):
        store = "DE/de"
        item = psn._get_item_for_cid(self.freeForPlusCid, store)

        print(
            "Using '"
            + item["name"]
            + "' ("
            + self.freeForPlusCid
            + ") from "
            + store
            + " for comparison. Item must be free for Plus members in order to pass the unit test. This might fail due to price changes"
        )

        assert item is not None

        normal_price = psn._get_normal_price(item)

        assert isinstance(normal_price, float)
        assert normal_price == 0

    @pytest.mark.skip(reason=NO_SEARCH_FOR_CID_REASON)
    def test_get_rewards_from_api(self):
        store = "DE/de"
        item = psn._get_item_for_cid("EP0006-CUSA02532_00-UNRAVELUNRAVEL09", store)
        assert len(psn._get_rewards(item)) > -1

    @unittest.skip("Skip temporary price reduction")
    def test_check_currently_reduced_item_all_prices(self):
        store = "DE/de"
        item = psn._get_item_for_cid("EP9000-CUSA04301_00-DREAMS0000000000", store)
        print("Checking: ", item["name"])
        assert psn._get_normal_price(item) == 39.99
        assert psn._get_playstation_plus_price_reduction(item) == 15.99
        assert psn._get_non_playstation_plus_price_reduction(item) == 15.99
        assert psn._get_price(item) == 15.99

    @unittest.skip("Skip temporary price reduction")
    def test_check_currently_reduced_item_no_plus_reduction(self):
        store = "DE/de"
        item = psn._get_item_for_cid("EP9000-CUSA00194_00-UNTILDAWN0000001", store)
        print("Checking: ", item["name"])
        assert psn._get_normal_price(item) == 59.99
        assert psn._get_playstation_plus_price_reduction(item) is None
        assert psn._get_non_playstation_plus_price_reduction(item) == 44.99
        assert psn._get_price(item) == 44.99

    def test_determine_storeFromCID(self):
        assert psn._determine_store("EP9000-CUSA00194_00-UNTILDAWN0000001") == "DE/de"
        assert psn._determine_store("JP0006-NPJB00377_00-BATTLEFIELD40000") == "JP/jp"
        assert psn._determine_store("UP2034-CUSA04841_00-NMSDIGITAL000001") == "US/en"
        assert psn._determine_store("1") is None

    def get_game(self, name="Bloodborne", id="EP9000-CUSA00207_00-BLOODBORNE0000EU"):
        game = self.psn.get_item_by(item_id=id)
        return game

    def test_format_items_to_json(self):
        game_offers = self.psn.search("Tearaway Unfolded")
        json_string = format_items_as_json(game_offers)
        assert "Tearaway" in json_string

    def test_get_item_by_search(self):
        game_offers = self.psn.search("Tearaway™ Unfolded")
        game_offer = game_offers[0]
        assert game_offer.name == "Tearaway™ Unfolded"
        assert game_offer.prices[0].offer_type == "discountedPrice" # Discounted price should be first
        assert game_offer.prices[0].value != 0  # Demo should not be first returned
        assert game_offer.prices[0].value != 100  # Price should not be 100 which is the PS Now dummy price

    def test_get_item_by_search_that_misses_price(self):
        game_offers = self.psn.search("Dreams")
        game_offer = game_offers[0]
        assert game_offer.prices[0].value >= 0
        assert game_offer.name == "Dreams™"

    def test_search_alot(self):
        game_offers = self.psn.search("park")
        print("\n".join(str(e) for e in game_offers))
        assert len(game_offers) > 1

    def test_search_test_without_playable_platforms(self):
        game_offers = self.psn.search("test")
        print("\n".join(str(e) for e in game_offers))
        assert len(game_offers) > 1

    @pytest.mark.skip(reason=NO_SEARCH_FOR_CID_REASON)
    def test_get_item_by_id(self):
        id = "EP9000-CUSA00562_00-TEARAWAYUNFOLDED"
        name = "Tearaway™ Unfolded"
        game_offer = self.psn.get_item_by(item_id=id)

        assert game_offer.name == name
        assert game_offer.id == id

    @pytest.mark.skip(reason=NO_SEARCH_FOR_CID_REASON)
    def test_get_item_by_id_has_picture(self):
        assert "http" in self.get_game().picture_url

    @pytest.mark.skip(reason=NO_SEARCH_FOR_CID_REASON)
    def test_mailfunc(self):
        mailalert("EP0177-CUSA07010_00-SONICMANIA000000,100.00", psnmailalert_main)
