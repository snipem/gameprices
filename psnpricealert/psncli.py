#!/usr/bin/env python

import sys
import logging
import argparse
import codecs
import locale

from psnpricealert.psn import psn
from psnpricealert.utils import utils

logging.basicConfig(
    filename="psnpricealert.log",
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)-8s] %(message)s",
    filemode = "w")

parser = argparse.ArgumentParser()
parser.add_argument("--id", "-i", help="CID of game to check")
parser.add_argument("--container", "-c", help="Container to list")
parser.add_argument("--store", "-s", help="Regional PSN store to check. Default: 'DE/de'", default="DE/de")
parser.add_argument("--price", "-p", help="Desired price of game", type=float)
parser.add_argument("--query", "-q", help="Name of item to search for")
parser.add_argument("--log", "-l", help="Write to log file", dest='log', action='store_true')

def checkWishPrice(cid, store, wishPrice):

    item = psn.getItemForCid(cid, store)
    normalPrice = psn.getPrice(item)
    name = psn.getName(item)

    if (normalPrice > wishPrice):
        utils.print_enc(("Wish price {0:.2f} for '"+name+"' does not yet match {1:.2f}, exiting").format(wishPrice, normalPrice))
        return False
    else:
        utils.print_enc(("Wish price {0:.2f} for '"+name+"' matched. Is now: {1:.2f}").format(wishPrice, normalPrice))
        return True

def formatItems(items):
    cids = []
    foundItems = []

    for item in items:
        try:
            logging.debug("Parsing:\n" + utils.prettyPrintJson(item))
            name = item['name']
            itemType = item['game_contentType']
            cid = item['id']
            price = str(psn.getPrice(item))

            platform = ", ".join(item['playable_platform'])
            foundItems.append((cid + "\t" + name + "\t" + platform + "\t" + price + "\t" + itemType))
            cids.append(cid)
        except Exception as e:
            logging.exception(e)

    return foundItems

def searchForItemsByNameAndFormatOutput(name, store):
    items = psn.searchForItemsByName(name, store)
    return formatItems(items)

def searchForItemsByContainerAndFormatOutput(container, store, filtersDict):
    items = psn.getItemsByContainer(container, store, filtersDict)
    return formatItems(items)

def main():
    args = parser.parse_args()

    if not args.log:
        logging.getLogger().disabled = True

    if (args.query != None and args.store != None):
        printString = searchForItemsByNameAndFormatOutput(args.query,args.store)
        if (len(printString) > 0):
            utils.print_enc("\n".join(printString))
            exit(0)
        else:
            exit(-1)
    elif (args.container != None and args.store != None):
        printString = searchForItemsByContainerAndFormatOutput(args.container, args.store, {"platform": "ps4"})
        if (len(printString) > 0):
            utils.print_enc("\n".join(printString))
            exit(0)
        else:
            exit(-1)

    elif (args.store != None and args.id != None and args.price != None):
        priceMatched = checkWishPrice(args.id, args.store, args.price)
        if (priceMatched):
            exit(0)
        else:
            exit(-1)

if __name__ == "__main__":
    main()
