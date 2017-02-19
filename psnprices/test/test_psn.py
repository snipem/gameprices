#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from psnprices.psn import psn


class MyTest(unittest.TestCase):

    # CID for item that is free for Plus members but not for normal members
    # TuneIt on german store
    freeForPlusCid = "EP4423-PCSB00407_00-TUNEIN0000000000"

    def test_searchForCidByTitleInGermanStore(self):
        cids = psn.getCidForName("Metal Gear", "DE/de")

        assert len(cids) > 0

    def test_searchForCidByTitleInUsStore(self):
        cids = psn.getCidForName("Metal Gear", "US/en")

        assert len(cids) > 0

    def test_getItemForCid(self):
        store = "DE/de"
        cids = psn.getCidForName("Tearaway", store)
        item = psn.getItemForCid(cids[0], store)

        assert item['name'] is not None

    def test_getItemForCid2(self):
        store = "DE/de"
        cids = psn.getCidForName("Child of Light", store)
        item = psn.getItemForCid(cids[0], store)

        assert item['name'] is not None

    def test_getItemByContainer(self):
        store = "DE/de"
        items = psn.getItemsByContainer(
            'STORE-MSF75508-PLUSINSTANTGAME', store, {"platform": "ps4"})

        assert len(items) > 0

    def test_getPlaystationPlusPrice(self):
        store = "DE/de"
        item = psn.getItemForCid(self.freeForPlusCid, store)

        print("Using '" + item['name'] + "' (" + self.freeForPlusCid + ") from " + store +
              " for comparison. Item must be free for Plus members in order to pass the unit test. This might fail due to price changes")

        assert item is not None

        normalPrice = psn.getPrice(item)
        plusPrice = psn.getPlaystationPlusPrice(item)

        print ("Normal Price: ", "%.2f" %
               normalPrice, "Plus Price: ", "%.2f" % plusPrice)

        assert type(normalPrice) is float
        assert type(plusPrice) is float
        assert plusPrice == 0

    def test_checkCurrencySymbolAsPartOfName(self):
        store = "DE/de"
        cids = psn.getCidForName("Child of Light", store)
        item = psn.getItemForCid(cids[0], store)
        assert psn.getDisplayPrice(item, store)[0] == u'\N{EURO SIGN}'

    def test_checkCurrencySymbol(self):
        assert psn.getCurrencySymbol("DE/de") == u'\N{EURO SIGN}'
        assert psn.getCurrencySymbol("US/en") == u'\N{DOLLAR SIGN}'
        assert psn.getCurrencySymbol("JP/jp") == u'\N{YEN SIGN}'
        assert psn.getCurrencySymbol("Unknown") == ''
    
    def test_getRewards(self):
        store = "DE/de"
        item = psn.getItemForCid("EP0006-CUSA02532_00-UNRAVELUNRAVEL09", store)
        assert len(psn.getRewards(item)) > -1

    @unittest.skip("Skip temporary price reduction")
    def test_checkCurrentlyReducedItem_AllPrices(self):
        store = "DE/de"
        item = psn.getItemForCid("EP2107-CUSA00327_00-DONTSTARVEPS4V01", store)
        print("Checking: ", item['name'])
        assert psn.getNormalPrice(item) == 13.99
        assert psn.getPlaystationPlusPrice(item) == 4.89
        assert psn.getNonPlaystationPlusPrice(item) == 6.99
        assert psn.getPrice(item) == 4.89

    @unittest.skip("Skip temporary price reduction")
    def test_checkCurrentlyReducedItem_NoPlusReduction(self):
        store = "DE/de"
        item = psn.getItemForCid("EP9000-CUSA00194_00-UNTILDAWN0000001", store)
        print("Checking: ", item['name'])
        assert psn.getNormalPrice(item) == 59.99
        assert psn.getPlaystationPlusPrice(item) == None
        assert psn.getNonPlaystationPlusPrice(item) == 44.99
        assert psn.getPrice(item) == 44.99

    def test_determineStoreFromCID(self):
        assert psn.determineStore("EP9000-CUSA00194_00-UNTILDAWN0000001") == "DE/de"
        assert psn.determineStore("JP0006-NPJB00377_00-BATTLEFIELD40000") == "JP/jp"
        assert psn.determineStore("UP2034-CUSA04841_00-NMSDIGITAL000001") == "US/en"
        assert psn.determineStore("1") == None 
