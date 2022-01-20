#!/usr/bin/env python

import argparse
import json
import logging
from typing import List

from gameprices.offer import GameOffer
from gameprices.shop import Shop
from gameprices.shops.eshop import Eshop
from gameprices.shops.psn import Psn
from gameprices.utils import utils
from gameprices.utils.utils import format_items_as_json, format_items_as_text

parser = argparse.ArgumentParser()
parser.add_argument("--id", "-i", help="CID of game to check")
parser.add_argument(
    "--store",
    "-s",
    help="Regional PSN store to check. Default: 'DE/de'",
    default="DE/de",
)
parser.add_argument("--price", "-p", help="Desired price of game", type=float)
parser.add_argument("--query", "-q", help="Name of item to search for")
parser.add_argument(
    "--json", "-j", dest="json", action="store_true", default=False, help="Print JSON"
)
parser.add_argument(
    "--log", "-l", help="Write to log file", dest="log", action="store_true"
)


def check_wish_price(shop: Shop, cid: str, wish_price: float) -> bool:
    item = shop.get_item_by(item_id=cid)
    normal_price = item.prices[0].value
    name = item.name

    if normal_price > wish_price:
        utils.print_enc(("Wish price {0:.2f} for '" + name + "' does not yet match {1:.2f}, exiting").format(wish_price,
                                                                                                             normal_price))
        return False
    else:
        utils.print_enc(
            ("Wish price {0:.2f} for '" + name + "' matched. Is now: {1:.2f}").format(
                wish_price, normal_price
            )
        )
        return True


def search_for_items_by_name_and_format_output(shop: Shop, name: str, print_json: bool):
    items = shop.search(name)
    if print_json:
        return format_items_as_json(items)
    else:
        return format_items_as_text(items)


def main(shop):
    args = parser.parse_args()

    if not args.log:
        logging.getLogger().disabled = True
    else:
        logging.basicConfig(
            filename="psnprices.log",
            level=logging.INFO,
            format="%(asctime)s [%(levelname)-8s] %(message)s",
            filemode="w",
        )

    if args.query is not None and args.store is not None:
        print_string = search_for_items_by_name_and_format_output(
            shop, args.query, args.json
        )
        if len(print_string) == 0:
            exit(-1)
        elif not args.json:
            utils.print_enc("\n".join(print_string))
            exit(0)
        elif args.json:
            print(print_string)
            exit(0)

    elif args.store is not None and args.id is not None and args.price is not None:
        price_matched = check_wish_price(shop, args.id, args.price)
        if price_matched:
            exit(0)
        else:
            exit(-1)


def eshop_main():
    main(Eshop("DE/de"))


def psn_main():
    main(Psn("DE/de"))
