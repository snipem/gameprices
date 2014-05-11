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
parser.add_argument("--cid", help="CID of game to check")
parser.add_argument("--store", help="regional PSN store to check")
parser.add_argument("--price", help="desired price of game", type=float)
parser.add_argument("--search", help="Name of item to search for")

def checkWishPrice(cid, store, wishPrice):

    item = psn.getItemForCid(cid, store)
    normalPrice = psn.getPrice(item)

    utils.print_enc(item['default_sku']['entitlements'][0]['name'] + " - " + str(normalPrice))
    currentPrice = float(item['default_sku']['price']) / 100

    if (currentPrice > wishPrice):
        utils.print_enc("Wish price {0:.2f} does not yet match {1:.2f}, exiting".format(wishPrice, currentPrice))
        return False
    else:
        utils.print_enc("Wish price %{0:.2f} matched. Is now: %{1:.2f}".format(wishPrice, currentPrice))
        return True

def searchForItemsByNameAndFormatOutput(name, store):
    links = psn.searchForItemsByName(name, store)
    cids = []
    foundItems = []

    for link in links:
        try:
            logging.debug("Parsing:\n" + utils.prettyPrintJson(link))
            name = link['name']
            itemType = link['default_sku']['name']
            cid = link['default_sku']['entitlements'][0]['id']
            platform = link['playable_platform']
        
            foundItems.append(cid + "\t" + name + "\t" + str(platform) + "\t" + itemType)
            cids.append(cid)
        except Exception as e:
            logging.warn("Got error '"+e+"'' while parsing\n" + prettyPrintJson(link))

    return foundItems

def main():
    args = parser.parse_args()

    if (args.search != None and args.store != None):
        printString = searchForItemsByNameAndFormatOutput(args.search,args.store)
        if (len(printString) > 0):
            utils.print_enc("\n".join(printString))
            exit(0)
        else:
            exit(-1)

    elif (args.store != None and args.cid != None and args.price != None):
        priceMatched = checkWishPrice(args.cid, args.store, args.price)
        if (priceMatched):
            exit(0)
        else:
            exit(-1)

if __name__ == "__main__":
    main()
