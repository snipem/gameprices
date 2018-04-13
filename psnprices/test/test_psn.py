#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from psnprices.shops import psn
from psnprices.shops.psn import Psn

from psnprices.cli.psnmailalert import main as psnmailalert_main
from . commons import mailalert

class MyTest(unittest.TestCase):

    # CID for item that is free for Plus members but not for normal members
    # TuneIt on german store
    freeForPlusCid = "EP4423-PCSB00407_00-TUNEIN0000000000"

    def test_searchForCidByTitleInGermanStore(self):
        cids = psn._getCidForName("Metal Gear", "DE/de")

        assert len(cids) > 0

    def test_searchForCidByTitleInUsStore(self):
        cids = psn._getCidForName("Metal Gear", "US/en")

        assert len(cids) > 0

    def test_getItemForCid(self):
        store = "DE/de"
        cids = psn._getCidForName("Tearaway", store)
        item = psn._getItemForCid(cids[0], store)

        assert item['name'] is not None

    def test_getItemForCid2(self):
        store = "DE/de"
        cids = psn._getCidForName("Child of Light", store)
        item = psn._getItemForCid(cids[0], store)

        assert item['name'] is not None

    def test_getItemByContainer(self):
        store = "DE/de"
        items = psn._getItemsByContainer(
            'STORE-MSF75508-PLUSINSTANTGAME', store, {"platform": "ps4"})

        assert len(items) > 0

    def test_getPlaystationPlusPrice(self):
        store = "DE/de"
        item = psn._getItemForCid(self.freeForPlusCid, store)

        print("Using '" + item['name'] + "' (" + self.freeForPlusCid + ") from " + store +
              " for comparison. Item must be free for Plus members in order to pass the unit test. This might fail due to price changes")

        assert item is not None

        normalPrice = psn._getPrice(item)
        plusPrice = psn._getPlaystationPlusPrice(item)

        print ("Normal Price: ", "%.2f" %
               normalPrice, "Plus Price: ", "%.2f" % plusPrice)

        assert type(normalPrice) is float
        assert type(plusPrice) is float
        assert plusPrice == 0

    def test_checkCurrencySymbolAsPartOfName(self):
        store = "DE/de"
        cids = psn._getCidForName("Child of Light", store)
        item = psn._getItemForCid(cids[0], store)
        assert psn._getDisplayPrice(item, store)[0] == u'\N{EURO SIGN}'

    def test_checkCurrencySymbol(self):
        assert psn._getCurrencySymbol("DE/de") == u'\N{EURO SIGN}'
        assert psn._getCurrencySymbol("US/en") == u'\N{DOLLAR SIGN}'
        assert psn._getCurrencySymbol("JP/jp") == u'\N{YEN SIGN}'
        assert psn._getCurrencySymbol("Unknown") == ''
    
    def test_getRewards(self):
        store = "DE/de"
        item = psn._getItemForCid("EP0006-CUSA02532_00-UNRAVELUNRAVEL09", store)
        assert len(psn._getRewards(item)) > -1

    @unittest.skip("Skip temporary price reduction")
    def test_checkCurrentlyReducedItem_AllPrices(self):
        store = "DE/de"
        item = psn._getItemForCid("EP2107-CUSA00327_00-DONTSTARVEPS4V01", store)
        print("Checking: ", item['name'])
        assert psn._getNormalPrice(item) == 13.99
        assert psn._getPlaystationPlusPrice(item) == 4.89
        assert psn._getNonPlaystationPlusPrice(item) == 6.99
        assert psn._getPrice(item) == 4.89

    @unittest.skip("Skip temporary price reduction")
    def test_checkCurrentlyReducedItem_NoPlusReduction(self):
        store = "DE/de"
        item = psn._getItemForCid("EP9000-CUSA00194_00-UNTILDAWN0000001", store)
        print("Checking: ", item['name'])
        assert psn._getNormalPrice(item) == 59.99
        assert psn._getPlaystationPlusPrice(item) == None
        assert psn._getNonPlaystationPlusPrice(item) == 44.99
        assert psn._getPrice(item) == 44.99

    def test_determineStoreFromCID(self):
        assert psn._determineStore("EP9000-CUSA00194_00-UNTILDAWN0000001") == "DE/de"
        assert psn._determineStore("JP0006-NPJB00377_00-BATTLEFIELD40000") == "JP/jp"
        assert psn._determineStore("UP2034-CUSA04841_00-NMSDIGITAL000001") == "US/en"
        assert psn._determineStore("1") == None 

class PsnTest(unittest.TestCase):

    psn = Psn(country="DE/de")

    def get_game(self, name="Bloodborne", id="EP9000-CUSA00207_00-BLOODBORNE0000EU"):
        game = self.psn.get_item_by(name=name,id=id)
        return game 

    def test_getItemForId(self):
        game_offers = self.psn.search("Tearaway™ Unfolded")
        game_offer = game_offers[0]
        assert game_offer.name == "Tearaway™ Unfolded"

    def test_search_alot(self):
        game_offers = self.psn.search("park")
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
