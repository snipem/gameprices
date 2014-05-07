playstation-price-drop-alert
============================

Command line tool for alerting price drops in the Sony Entertainment Network aka Playstation Network

Description
-----------
The Sony Entertainment Network (SEN) uses CIDs to identify items in it's catalogue. In order to alert you on the desired price of an SEN you need the CID. Use your Browser (cid GET parameter in URL) or this script (--search) to retrieve the CID.

In order to check the price of an item. You need a store identifier. These store identifiers are known to work:

* DE/de
* GB/en
* US/en

Prices are always in the local currency. Therefore it is € for DE/de and £ for GB/en.

Usage
-----
	usage: psnpricealert.py [-h] [--cid CID] [--store STORE] [--price PRICE]
	                        [--search SEARCH]

	optional arguments:
	  -h, --help       show this help message and exit
	  --cid CID        CID of game to check
	  --store STORE    regional PSN store to check
	  --price PRICE    desired price of game
	  --search SEARCH  Name of item to search for

Example
-------
You may run this script with the following command lines:

### Searching for the CID of an item

Define the name of a game and the store.

	python psnpricealert.py --search "metal gear solid peace walker psp" --store DE/de

You will get a result containing one to many search results with the CID. The first output of each search line is the CID, the second the name, the third the supported systems and the last is a description of the item type in the local store language. It is "Vollversion" here which means "full version" in German.

	EP0101-ULES01372_00-GPCMETALGE000001	Metal Gear Solid: Peace Walker [PSP]	[u'PS Vita', u'PSP\xae']	Vollversion

### Check if desired price has been met

The price is in local currency. As exit statuses render the outcome of the alert, you may send you e-mails or desktop notifications with "&&" or "||". In this example, there is a string printed to the console.

	python psnpricealert.py --cid EP0101-ULES01372_00-GPCMETALGE000001 --store DE/de --price 15.00 &&
	echo "Price matched, let's buy Metal Gear Solid PW"