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

Define the name of a game and the store. Get a CID as result, will return EP0101-ULES01372_00-GPCMETALGE000001

	python psnpricealert.py --search "metal gear solid peace walker psp" --store DE/de ||
	echo "Did not find a unique CID. See log for further details. Be more precise"

Check if desired price has been met. Price is in local currency. As exit statuses render the outcome of the alert, you may send you e-mails or desktop notifications with "&&" or "||". In this example, there is a string printed to the console.

	python psnpricealert.py --cid EP0101-ULES01372_00-GPCMETALGE000001 --store DE/de --price 15.00 &&
	echo "Price matched, let's buy Metal Gear Solid PW"