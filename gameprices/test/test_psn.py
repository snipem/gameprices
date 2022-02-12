#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from gameprices.shops import psn
from gameprices.shops.psn import Psn
from gameprices.cli import *

from gameprices.cli.mailalert import main as psnmailalert_main
from gameprices.test.commons import mailalert
from gameprices.utils.utils import format_items_as_json


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
        item = psn._get_item_for_cid(cids[0], store)

        assert item["name"] is not None

    def test_get_item_for_cid2(self):
        store = "DE/de"
        cids = psn._get_cid_for_name("Child of Light", store)
        item = psn._get_item_for_cid(cids[0], store)

        assert item["name"] is not None

    def test_get_item_by_container(self):
        store = "DE/de"
        items = psn._get_items_by_container(
            "STORE-MSF75508-PLUSINSTANTGAME", store, {"platform": "ps4"}
        )

        assert len(items) > 0

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

    def test_get_rewards_from_api(self):
        store = "DE/de"
        item = psn._get_item_for_cid("EP0006-CUSA02532_00-UNRAVELUNRAVEL09", store)
        assert len(psn._get_rewards(item)) > -1

    def test_get_rewards_from_string(self):
        item = {
            'skus': [{'amortizeFlag': False, 'bundleExclusiveFlag': False, 'chargeImmediatelyFlag': False,
                      'charge_type_id': 0, 'credit_card_required_flag': 0, 'defaultSku': True,
                      'display_price': '€49,99', 'eligibilities': [], 'entitlements': [
                    {'description': None, 'drms': [], 'duration': 0, 'durationOverrideTypeId': None,
                     'exp_after_first_use': 0, 'feature_type_id': 3, 'id': 'PILLARS-CID',
                     'license_type': 0, 'metadata': {'voiceLanguageCode': ['en'],
                                                     'subtitleLanguageCode': ['de', 'ru', 'en', 'it', 'fr', 'pl',
                                                                              'es']},
                     'name': 'Pillars of Eternity: Complete Edition', 'packageType': 'PS4GD',
                     'packages': [{'platformId': 13, 'platformName': 'ps4', 'size': 151248}],
                     'preorder_placeholder_flag': False, 'size': 0, 'subType': 0,
                     'subtitle_language_codes': ['de', 'ru', 'en', 'it', 'fr', 'pl', 'es'], 'type': 5, 'use_count': 0,
                     'voice_language_codes': ['en']}], 'id': 'PILLARS-CID',
                      'is_original': False, 'name': 'Vollversion', 'platforms': [0, 18, 10, 13], 'price': 4999,
                      'rewards': [{'id': 'ID_CAMPAIGN_1', 'discount': 70, 'price': 1499, 'reward_type': 2,
                                   'display_price': '€14,99', 'isPlus': False, 'campaigns': [
                              {'id': 'ID_CAMPAIGN_2', 'start_date': '2022-02-02T00:00:00Z',
                               'end_date': '2022-02-16T23:59:00Z'}], 'bonus_discount': 80,
                                   'bonus_entitlement_id': 'PLUS_ENTITLEMENT_ID', 'bonus_price': 999,
                                   'reward_source_type_id': 2, 'start_date': '2022-02-02T00:00:00Z',
                                   'end_date': '2022-02-16T23:59:00Z', 'bonus_display_price': '€9,99'}],
                      'seasonPassExclusiveFlag': False, 'skuAvailabilityOverrideFlag': False, 'sku_type': 0,
                      'type': 'standard'}]
        }
        assert psn._get_all_prices(item) == [49.99, 14.99, 9.99]
        assert psn._get_normal_price(item) == 49.99
        assert psn._get_playstation_plus_price_reduction(item) == 9.99
        assert psn._get_non_playstation_plus_price_reduction(item) == 14.99

    def test_get_rewards_from_string_with_demo_and_psnow(self):
        item = {
            'skus': [{'amortizeFlag': True, 'bundleExclusiveFlag': False, 'chargeImmediatelyFlag': False,
                      'charge_type_id': 0, 'credit_card_required_flag': 0, 'defaultSku': True,
                      'display_price': '€100,00', 'eligibilities': [], 'entitlements': [
                    {'description': None, 'drms': [], 'duration': 1800, 'durationOverrideTypeId': None,
                     'exp_after_first_use': 0, 'feature_type_id': 3, 'id': 'TEARAWAY_CID',
                     'license_type': 0, 'metadata': {
                        'voiceLanguageCode': ['de', 'no', 'fi', 'ru', 'sv', 'pt', 'en', 'it', 'fr', 'es', 'pl', 'da',
                                              'nl'],
                        'subtitleLanguageCode': ['de', 'no', 'fi', 'sv', 'ru', 'pt', 'en', 'it', 'fr', 'es', 'pl', 'da',
                                                 'nl']}, 'name': 'Tearaway™ Unfolded', 'packageType': 'PS4GD',
                     'packages': [{'platformId': 13, 'platformName': 'ps4', 'size': 77712}],
                     'preorder_placeholder_flag': False, 'size': 0, 'subType': 0,
                     'subtitle_language_codes': ['de', 'no', 'fi', 'sv', 'ru', 'pt', 'en', 'it', 'fr', 'es', 'pl', 'da',
                                                 'nl'], 'type': 5, 'use_count': 0,
                     'voice_language_codes': ['de', 'no', 'fi', 'ru', 'sv', 'pt', 'en', 'it', 'fr', 'es', 'pl', 'da',
                                              'nl']}], 'id': 'TEARAWAY_CID',
                      'is_original': False, 'name': 'PS Now Download Game', 'platforms': [0, 18, 10, 13],
                      'price': 10000, 'rewards': [
                    {'id': 'ID2', 'entitlement_id': 'IP9102-NPIA90011_01-RWD-104513',
                     'service_provider_id': 'ID3', 'discount': 100, 'price': 0, 'reward_type': 2,
                     'display_price': 'Kostenlos', 'name': 'PS Now -- Discount 100% Off', 'isPlus': False,
                     'rewardSourceId': 3, 'reward_source_type_id': 1, 'start_date': '2000-01-01T00:00:00Z'}],
                      'seasonPassExclusiveFlag': False, 'skuAvailabilityOverrideFlag': False, 'sku_type': 0,
                      'type': 'standard'},
                     {'amortizeFlag': False, 'bundleExclusiveFlag': False, 'chargeImmediatelyFlag': False,
                      'charge_type_id': 0, 'credit_card_required_flag': 0, 'display_price': '€19,99',
                      'eligibilities': [], 'entitlements': [
                         {'description': None, 'drms': [], 'duration': 0, 'durationOverrideTypeId': None,
                          'exp_after_first_use': 0, 'feature_type_id': 3, 'id': 'TEARAWAY_CID',
                          'license_type': 0, 'metadata': {
                             'voiceLanguageCode': ['de', 'no', 'fi', 'ru', 'sv', 'pt', 'en', 'it', 'fr', 'es', 'pl',
                                                   'da', 'nl'],
                             'subtitleLanguageCode': ['de', 'no', 'fi', 'sv', 'ru', 'pt', 'en', 'it', 'fr', 'es', 'pl',
                                                      'da', 'nl']}, 'name': 'Tearaway™ Unfolded',
                          'packageType': 'PS4GD',
                          'packages': [{'platformId': 13, 'platformName': 'ps4', 'size': 70937}],
                          'preorder_placeholder_flag': False, 'size': 0, 'subType': 0,
                          'subtitle_language_codes': ['de', 'no', 'fi', 'sv', 'ru', 'pt', 'en', 'it', 'fr', 'es', 'pl',
                                                      'da', 'nl'], 'type': 5, 'use_count': 0,
                          'voice_language_codes': ['de', 'no', 'fi', 'ru', 'sv', 'pt', 'en', 'it', 'fr', 'es', 'pl',
                                                   'da', 'nl']}], 'id': 'TEARAWAY_CID',
                      'is_original': False, 'name': 'Vollversion', 'platforms': [0, 18, 10, 13], 'price': 1999,
                      'rewards': [], 'seasonPassExclusiveFlag': False, 'skuAvailabilityOverrideFlag': False,
                      'sku_type': 0, 'type': 'standard'}]
        }
        assert psn._get_all_prices(item) == [19.99]
        assert psn._get_normal_price(item) == 19.99
        assert psn._get_playstation_plus_price_reduction(item) == None
        assert psn._get_non_playstation_plus_price_reduction(item) == None

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

    def test_get_item_for_id(self):
        game_offers = self.psn.search("Tearaway™ Unfolded")
        game_offer = game_offers[0]
        assert game_offer.name == "Tearaway™ Unfolded"
        assert game_offer.prices[0].offer_type == "NORMAL" # Normal price should be first
        assert game_offer.prices[0].value != 0  # Demo should not be first returned
        assert game_offer.prices[0].value != 100  # Price should not be 100 which is the PS Now dummy price

    def test_get_item_for_id_that_misses_price(self):
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

    def test_get_item_by_id(self):
        id = "EP9000-CUSA00562_00-TEARAWAYUNFOLDED"
        name = "Tearaway™ Unfolded"
        game_offer = self.psn.get_item_by(item_id=id)

        assert game_offer.name == name
        assert game_offer.id == id

    def test_game_has_picture(self):
        assert "http" in self.get_game().picture_url

    def test_mailfunc(self):
        mailalert("EP0177-CUSA07010_00-SONICMANIA000000,100.00", psnmailalert_main)
