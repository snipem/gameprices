#!/bin/sh
#Tell python that our terminal is able to understand UTF-8
export PYTHONIOENCODING=utf-8

#Define the name of a game and the store
./psncli.py --query "metal gear solid peace walker psp" --store DE/de

#Or even shorther, because DE/de is the default store
./psncli.py -q "metal gear solid peace walker psp"

#Check if desired price has been met. Price is in local currency
./psncli.py --id EP0101-ULES01372_00-GPCMETALGE000001 --store DE/de --price 15.00 &&
echo "Price matched, let's buy Metal Gear Solid PW"

#Check if desired price for Sportfriends on the Swedish store has been met and send an notifcation through the notification center of OS X
./psncli.py --id EP4471-CUSA00484_00-SPORTSFRIENDS000 --store SE/en --price 130 &&
osascript -e 'display notification "Sportfriends is now less than 130 kr"'

#Search for PS4 demos on US store
./psncli.py -c STORE-MSF77008-NEWPS4DEMOSCATEG -s US/en
