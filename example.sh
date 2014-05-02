#!/bin/sh

#Define the name of a game and the store. Get a CID as result, will return EP0101-ULES01372_00-GPCMETALGE000001
python psnpricealert.py --search "metal gear solid peace walker psp" --store DE/de || echo "Did not find a unique CID. See log for further details. Be more precise"

#Check if desired price has been met. Price is in local currency
python psnpricealert.py --cid EP0101-ULES01372_00-GPCMETALGE000001 --store DE/de --price 15.00 && echo "Price matched, let's buy Metal Gear Solid PW"