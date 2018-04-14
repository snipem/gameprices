#!/usr/bin/env python

import sys
import logging
import argparse
import codecs
import locale

from gameprices.shops import psn
from gameprices.shops.eshop import Eshop
from gameprices.shops.psn import Psn
from gameprices.utils import utils

logging.basicConfig(
    filename="psnprices.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-8s] %(message)s",
    filemode="w")

parser = argparse.ArgumentParser()
parser.add_argument("--id", "-i", help="CID of game to check")
parser.add_argument("--container", "-c", help="Container to list")
parser.add_argument(
    "--store",
    "-s",
    help="Regional PSN store to check. Default: 'DE/de'",
    default="DE/de")
parser.add_argument("--price", "-p", help="Desired price of game", type=float)
parser.add_argument("--query", "-q", help="Name of item to search for")
parser.add_argument(
    "--log",
    "-l",
    help="Write to log file",
    dest='log',
    action='store_true')

shop = None

def check_wish_price(cid, store, wishPrice):

    item = psn._getItemForCid(cid, store)
    normalPrice = item.price[0].value
    name = item.name

    if (normalPrice > wishPrice):
        utils.print_enc(
            ("Wish price {0:.2f} for '" +
             name +
             "' does not yet match {1:.2f}, exiting").format(
                wishPrice,
                normalPrice))
        return False
    else:
        utils.print_enc(
            ("Wish price {0:.2f} for '" +
             name +
             "' matched. Is now: {1:.2f}").format(
                wishPrice,
                normalPrice))
        return True


def format_items(items):
    cids = []
    foundItems = []

    for item in items:
        try:
            name = item.name
            itemType = item.type
            cid = item.cid
            price = str(item.prices[0].value) if len(item.prices) > 0 else ""

            platform = ",".join(item.platforms)
            foundItems.append(
                (cid +
                 "\t" +
                 name +
                 "\t" +
                 platform +
                 "\t" +
                 price +
                 "\t" +
                 itemType))
            cids.append(cid)
        except Exception as e:
            logging.exception(e)

    return foundItems


def search_for_items_by_name_and_format_output(name, store):
    items = shop.search(name)
    return format_items(items)


def search_for_items_by_container_and_format_output(
        container, store, filtersDict):
    items = psn._get_items_by_container(container, store, filtersDict)
    return format_items(items)


def main(inshop):

    global shop
    shop = inshop

    args = parser.parse_args()

    if not args.log:
        logging.getLogger().disabled = True

    if (args.query is not None and args.store is not None):
        printString = search_for_items_by_name_and_format_output(
            args.query, args.store)
        if (len(printString) > 0):
            utils.print_enc("\n".join(printString))
            exit(0)
        else:
            exit(-1)
    elif (args.container is not None and args.store is not None):
        printString = search_for_items_by_container_and_format_output(
            args.container, args.store, {"platform": "ps4"})
        if (len(printString) > 0):
            utils.print_enc("\n".join(printString))
            exit(0)
        else:
            exit(-1)

    elif (args.store is not None and args.id is not None and args.price is not None):
        priceMatched = check_wish_price(args.id, args.store, args.price)
        if (priceMatched):
            exit(0)
        else:
            exit(-1)


def eshop_main():
    main(Eshop("DE/de"))


def psn_main():
    main(Psn("DE/de"))
