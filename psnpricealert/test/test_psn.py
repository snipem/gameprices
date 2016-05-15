import unittest
from psnpricealert.psn import psn

class MyTest(unittest.TestCase):


	### CID for item that is free for Plus members but not for normal members
	# TuneIt on german store
	freeForPlusCid = "EP4423-PCSB00407_00-TUNEIN0000000000"

	def test_searchForCidByTitleInGermanStore(self):
		cids = psn.getCidForName("Metal Gear","DE/de")

		assert len(cids) > 0

	def test_searchForCidByTitleInUsStore(self):
		cids = psn.getCidForName("Metal Gear","US/en")

		assert len(cids) > 0

	def test_getItemForCid(self):
		store = "DE/de"
		cids = psn.getCidForName("Tearaway",store)
		item = psn.getItemForCid(cids[0],store)

		assert item['name'] is not None

	def test_getItemForCid2(self):
		store = "DE/de"
		cids = psn.getCidForName("Child of Light",store)
		item = psn.getItemForCid(cids[0],store)

		assert item['name'] is not None

	def test_getItemByContainer(self):
		store = "DE/de"
		items = psn.getItemsByContainer('STORE-MSF75508-PLUSINSTANTGAME',store, {"platform": "ps4"})

		assert len(items) > 0

	def test_getPlaystationPlusPrice(self):
		store = "DE/de"
		item = psn.getItemForCid(self.freeForPlusCid,store)

		print("Using '"+item['name']+"' ("+self.freeForPlusCid+") from "+store+" for comparison. Item must be free for Plus members in order to pass the unit test. This might fail due to price changes")

		assert item is not None

		normalPrice = psn.getPrice(item)
		plusPrice = psn.getPlaystationPlusPrice(item)

		print ("Normal Price: " , "%.2f" % normalPrice, "Plus Price: ", "%.2f" % plusPrice)

		assert type(normalPrice) is float
		assert type(plusPrice) is float
		assert plusPrice == 0
	