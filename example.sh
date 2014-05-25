#!/bin/sh
#Tell python that our terminal is able to understand UTF-8
export PYTHONIOENCODING=utf-8

#Define the name of a game and the store
./psncli.py --search "metal gear solid peace walker psp" --store DE/de

#Check if desired price has been met. Price is in local currency
./psncli.py --cid EP0101-ULES01372_00-GPCMETALGE000001 --store DE/de --price 15.00 &&
echo "Price matched, let's buy Metal Gear Solid PW"
