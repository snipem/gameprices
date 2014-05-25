playstation-price-drop-alert
============================
[![Build Status](https://travis-ci.org/snipem/playstation-price-drop-alert.svg?branch=master)](https://travis-ci.org/snipem/playstation-price-drop-alert)

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

### Mail alerting

Just run `python psnmailalert.py` for mail alerting. See example below.

### Command line interface
	usage: psncli.py [-h] [--cid CID] [--store STORE] [--price PRICE]
	                 [--query QUERY]

	optional arguments:
	  -h, --help            show this help message and exit
	  --cid CID, -c CID     CID of game to check
	  --store STORE, -s STORE
	                        regional PSN store to check. Default: 'DE/de'
	  --price PRICE, -p PRICE
	                        desired price of game
	  --query QUERY, -q QUERY
	                        Name of item to search for

#### Retrieving UTF-8 encoded output on terminals
You may have to tell Python that your terminal is capable of dealing with UTF-8 outputs. Some PSN items are annoted with trademark, copyright or foreign language specific symbols. To do so set `export PYTHONIOENCODING=utf-8` in your terminal window. 


Example
-------
You may run this script with the following command line variants:

### Mail alerting - Get a mail when alerts have been met

With `psnmailalert.py` you may set alerts for price drops in the `alerts.csv` file. The first value is the CID for the item, the second is the price to be matched in order to alert you by mail, and the second value is the store to search in. You may mix stores in the `alerts.csv`. After a price has been matched, the alert is removed from `alerts.csv`. You will not get any further alerts for that item.

	EP0001-NPEJ00305_00-B000000000001030,19.00,DE/de
	EP0101-ULES01372_00-GPCMETALGE000001,10.00,DE/de

 In order to receive mails you have to set your account settings in the file `mailconfig.json`. See `mailconfig.json_example` for an example config.

 To run `psnmailalert.py`, just type:

 	./psnmailalert.py

### Searching for the CID of an item

Define the name of a game and the store.

	./psncli.py --query "metal gear solid peace walker psp" --store DE/de

You will get a result containing one to many search results with the CID. The first output of each search line is the CID, the second the name, the third the supported systems and the last is a description of the item type in the local store language. It is "Vollversion" here which means "full version" in German.

	EP0101-ULES01372_00-GPCMETALGE000001	Metal Gear Solid: Peace Walker [PSP]	PS Vita, PSP®	19.99	Vollversion

### Check if desired price has been met

The price is in local currency. As exit statuses render the outcome of the alert, you may send you e-mails or desktop notifications with `&&` or `||`. In this example, there is a string printed to the console.

	./psncli.py --cid EP0101-ULES01372_00-GPCMETALGE000001 --store DE/de --price 15.00 &&
	echo "Price matched, let's buy Metal Gear Solid PW"


![Mail with alerts](res/mail.png?raw=true "Mail with alerts")
