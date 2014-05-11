from psnpricealert.psn import psn

def test_searchForCidByTitleInGermanStore():
	
	cids = psn.getCidForName("Metal Gear","DE/de")
	assert len(cids) > 0

def test_searchForCidByTitleInUsStore():
	
	cids = psn.getCidForName("Metal Gear","US/en")
	assert len(cids) > 0

def test_getItemForCid():
	store = "DE/de"
	cids = psn.getCidForName("Tearaway",store)
	item = psn.getItemForCid(cids[0],store)
	assert item['name'] is not None
