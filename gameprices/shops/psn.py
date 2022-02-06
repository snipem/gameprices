import datetime
import json
import logging
import re
import sys
import urllib.request
from typing import List
from urllib.parse import quote

from lxml import etree

from gameprices.offer import GameOffer, Price
from gameprices.shop import Shop
from gameprices.utils import utils

api_root = "https://store.playstation.com"
store_root = api_root
fetch_size = "99999"
appendix = ""
api_version = "19"

version = sys.version_info[0]

""" Dictionary object containing data specific to a Country store. The key is the store identifier per the
PSN API. The array of parameters contains [0]: the country-code folder for the PSN Store URL and
[1]: The character preceding each marketplaces CID """
store_code_mappings = {
    "DE/de": ["de-de", "E"],
    "NL/nl": ["nl-nl", "E"],
    "US/en": ["us-en", "U"],
    "JP/jp": ["jp-jp", "J"],
}


def _filter_none(item):
    if item is None:
        return False
    else:
        return True


def _get_item_for_cid(cid, store):
    try:
        url = (api_root + "/viewfinder/" + store + "/" + api_version + "/" + cid + "?size=" + fetch_size)
        data = utils.get_json_response(url)
        return data
    except Exception as e:
        logging.error("Got error '" + str(e) + "' while retrieving cid '" + cid + "' in store " + store)
        return None


def _get_rewards(item):
    rewards = []

    for sku in item["skus"]:
        if "defaultSku" in sku and sku["defaultSku"] == True and "rewards" in sku:
            for reward in sku["rewards"]:
                rewards.append(reward)

    return rewards


def _get_display_price(item, store):
    price = _get_price(item)
    display_price = store_code_mappings[store][1] + str(price)

    return display_price


def _get_cheapest_price(prices):
    return sorted(filter(_filter_none, prices))[0]


def _get_price(item):
    normal_price = _get_normal_price(item)
    non_playstation_plus_price = _get_non_playstation_plus_price(item)
    playstation_plus_price = _get_playstation_plus_price(item)

    return _get_cheapest_price(
        [normal_price, non_playstation_plus_price, playstation_plus_price]
    )


def _get_normal_price(item):
    for sku in item["skus"]:
        if "defaultSku" in sku and sku["defaultSku"] == True:
            return float(sku["price"]) / 100

    return None


def _get_non_playstation_plus_price(item):
    for reward in _get_rewards(item):
        if not reward.get("is_plus"):
            return float(reward.get("price")) / 100


def _get_playstation_plus_price(item):
    for reward in _get_rewards(item):
        if reward.get("bonus_price") is not None:
            return float(reward.get("bonus_price")) / 100
        else:
            return float(reward.get("price")) / 100

    return None


def _get_name(item):
    return item["name"]


def _get_image(item):
    if len(item["images"]) > 0:
        return item["images"][0]["url"]


def _get_offer_end_date(item):
    """ Returns the Offer End Date for a given Item
        :param item: The item for which the Offer End Date is to be retrieved
        :return: A datetime object which is the Offer End Date """

    if item["skus"][0] is not None:
        if "end_date" in item["skus"][0]:
            end_date = item["skus"][0]["end_date"]
            if end_date is not None:
                return datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ")


def _get_store_url(item, store):
    cid = item["id"]

    url = store_root + "/" + store_code_mappings[store][0] + "/cid=" + cid

    return url


def _get_cid_for_name(name, store):
    links = _search_for_items_by_name(name, store)
    cids = []

    for link in links:
        logging.debug("Parsing:\n" + utils.pretty_print_json(link))
        name = link["name"]
        item_type = link["top_category"]
        cid = link["id"]
        platform = ", ".join(link["playable_platform"])

        logging.info("Found: " + name + " - " + cid + " - Platform: " + platform + " - Type: " + item_type)
        cids.append(cid)

    return cids


def _get_next_data_respose(url):
    response = urllib.request.urlopen(url)
    html_response = response.read()
    encoding = response.headers.get_content_charset('utf-8')
    decoded_html = html_response.decode(encoding)

    html = etree.HTML(decoded_html)
    # h = etree.tostring(html, pretty_print=True, encoding=encoding, method="html").decode()

    from cssselect import GenericTranslator, SelectorError
    try:
        expression = GenericTranslator().css_to_xpath('#__NEXT_DATA__')
    except SelectorError:
        print('Invalid selector.')

    selection = [''.join(e.itertext()) for e in html.xpath(expression)]
    return json.loads(selection[0])


def _search_for_items_by_name(name: str, store: str) -> List[GameOffer]:
    encoded_name = quote(name)
    url = Psn._build_api_url(country=store, query=encoded_name)
    data = _get_next_data_respose(url)
    items = data["props"]["apolloState"]
    game_offers = _items_to_game_offers(items, country=store)
    return game_offers


def _items_to_game_offers(items: List, country: str) -> List[GameOffer]:
    return_list: List[GameOffer] = []

    for i in items:
        if "npTitleId" in items[i]:
            # This is a game
            price_id = items[i]['price']['id']
            g = GameOffer(
                name=items[i]["name"],
                id=items[i]["id"],
                cid=items[i]["id"],
                url="%s/%s/product/%s" % (store_root, country, items[i]["id"]),
                prices=[
                    Price(
                        value=_get_price_value_from_price_string(items[price_id]["discountedPrice"]),
                        offer_type="discountedPrice"
                    ),
                    Price(
                        value=_get_price_value_from_price_string(items[price_id]["basePrice"]),
                        offer_type="basePrice"
                    ),
                ],
                type=items[i]["storeDisplayClassification"],
                platforms=items[i]["platforms"]["json"]
            )
            return_list.append(g)

    return return_list


def _determine_store(cid: str) -> str:
    for store in store_code_mappings:
        store_code_mapping = store_code_mappings.get(store)

        if len(store_code_mapping) >= 2 and cid.startswith(
                store_code_mappings.get(store)[1]
        ):
            return store


def _get_items_by_container(container, store, filters_dict):
    url = api_root + "/viewfinder/" + store + "/" + api_version + "/" + container + "?size=" + fetch_size

    for i in filters_dict:
        url = url + "&" + quote(i) + "=" + quote(filters_dict[i])

    data = utils.get_json_response(url)
    links = data["links"]

    return links


def _get_price_value_from_price_string(price: str) -> float:
    try:
        return float(re.sub("[^0-9,\.,\,]", "", price).replace(",", "."))
    except Exception:
        return -1


class Psn(Shop):
    @staticmethod
    def _build_api_url(country, query):
        # TODO make safe for countries not in map
        return "%s/%s/search/%s" % (api_root, store_code_mappings.get(country)[0], query)

    def _item_to_game_offer(self, game):
        if not game:
            raise Exception("Item is empty")

        normal_price = _get_normal_price(game)
        plus_price = _get_playstation_plus_price(game)

        prices = []

        if normal_price:
            prices.append(Price(
                value=normal_price,
                offer_type="NORMAL",
            ))

        if plus_price:
            prices.append(Price(
                value=plus_price,
                offer_type="PS+",
            ))

        # Make lowest price first in list
        prices.sort(key=lambda x: x.value)

        return GameOffer(
            id=game["id"],
            cid=game["id"],
            url=game["url"],
            type=game["gameContentTypesList"][0]["key"]
            if "gameContentTypesList" in game
            else None,
            name=game["name"],
            prices=prices,
            platforms=game["playable_platform"] if "playable_platform" in game else "",
            picture_url=_get_image(game),
        )

    def search(self, name):
        game_offers = _search_for_items_by_name(name=name, store=self.country)
        # return_offers = []
        # for item in items:
        #     if 'bucket' in item and item['bucket'] == 'games':  # Only add items that are games and have prices etc.
        #         return_offers.append(self._item_to_game_offer(item))
        # return return_offers
        return game_offers

    def get_item_by(self, item_id):
        item = _get_item_for_cid(item_id, self.country)
        return self._item_to_game_offer(item)
