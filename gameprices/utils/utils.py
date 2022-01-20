import json
import urllib.request
from typing import List

from gameprices.offer import GameOffer
from gameprices.price import Price


def get_json_file(filename):
    json_data = open(filename)
    data = json.load(json_data)
    json_data.close()
    return data


def get_json_response(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())


def pretty_print_json(json_string):
    return json.dumps(json_string, sort_keys=True, indent=4, separators=(",", ": "))


def print_enc(s):
    print(s.decode("utf-8") if isinstance(s, type(b"")) else s)


def get_lowest_price(game_offer: GameOffer) -> Price:
    if len(game_offer.prices) == 0:
        return Price(offer_type="NONE", value=-1)

    prices = game_offer.prices
    prices.sort(key=lambda x: x.value)
    return prices[0]


def format_items_as_text(items: List[GameOffer]) -> List[str]:
    cids = []
    found_items = []

    for item in items:
        name = item.name
        item_type = item.type
        cid = item.cid
        lowest_price = get_lowest_price(item)

        platform = ",".join(item.platforms)
        found_items.append(f"{cid}\t{name}\t{platform}\t{lowest_price.value:.2f}\t{item_type}")
        cids.append(cid)

    return found_items


def format_items_as_json(items: List[GameOffer]) -> str:
    return json.dumps([o.dump() for o in items])
