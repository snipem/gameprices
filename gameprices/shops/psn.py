import datetime
import logging
import sys
from urllib.parse import quote

from gameprices.offer import GameOffer, Price
from gameprices.shop import Shop
from gameprices.utils import utils

api_root = "https://store.playstation.com/chihiro-api"
store_root = "https://store.playstation.com/#!"
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
        if "rewards" in sku:
            for reward in sku["rewards"]:
                rewards.append(reward)

    return rewards


def _get_all_prices(item):
    # Returns all prices, regardless of their semantics

    prices = []  # highest to lowest
    has_free_offer = False

    for sku in item["skus"]:
        p = float(sku["price"]) / 100
        if p != 0 and p != 100:  # 0 is likely demo, 100 is likely PS Now offering
            prices.append(p)
        elif p == 0:
            has_free_offer = True

    for reward in _get_rewards(item):
        p = float(reward.get("price")) / 100
        if p != 0 and p != 100:  # 0 is likely demo, 100 is likely PS Now offering
            prices.append(p)
        elif p == 0:
            has_free_offer = True

        if "bonus_price" in reward:
            p = float(reward.get("bonus_price")) / 100
            prices.append(p)

    prices.sort(key=lambda x: x, reverse=True)

    if len(prices) == 0 and has_free_offer:
        # If there were no other prices found and there was found
        # a 0 price before, expect this to be a free item and no demo
        prices.append(0.0)

    return prices


def _get_normal_price(item):
    """Returns the highest price of the item as the normal non reduced price"""
    prices = _get_all_prices(item)
    if len(prices) > 0:
        return prices[0]
    else:
        return None


def _get_non_playstation_plus_price_reduction(item):
    """Returns the middle price of the item as the non playstation plus reduced price"""
    prices = _get_all_prices(item)
    if len(prices) == 3: # Has normal, non ps plus and ps plus price
        return prices[1]
    elif len(prices) == 2:
        return prices[len(prices) - 1] # return last price as non ps plus price
    else:
        return None


def _get_playstation_plus_price_reduction(item):
    """Returns the lowest price as the playstation plus price reduction of the item"""
    prices = _get_all_prices(item)
    if len(prices) == 3:
        return prices[len(prices) - 1] # Expect ps plus always to be the lowest on three prices
    elif len(prices) == 2:
        return prices[1]
    else:
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


def _search_for_items_by_name(name, store):
    encoded_name = quote(name)
    url = api_root + "/bucket-search/" + store + "/" + api_version + "/" + encoded_name + "?size=" + fetch_size + "&start=0"
    data = utils.get_json_response(url)
    links = data["categories"]["games"]["links"]
    return links


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


class Psn(Shop):
    @staticmethod
    def _build_api_url(country, query):
        return "%s/%s/select?q=%s&%s" % (api_root, country, query, appendix)

    def _item_to_game_offer(self, game):
        if not game:
            raise Exception("Item is empty")

        normal_price = _get_normal_price(game)
        plus_price = _get_playstation_plus_price_reduction(game)
        non_plus_price = _get_non_playstation_plus_price_reduction(game)

        prices = []

        if normal_price != None:
            prices.append(Price(
                value=normal_price,
                offer_type="NORMAL",
            ))

        if plus_price != None:
            prices.append(Price(
                value=plus_price,
                offer_type="PS+",
            ))

        if non_plus_price != None:
            prices.append(Price(
                value=non_plus_price,
                offer_type="Without PS+",
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
        items = _search_for_items_by_name(name=name, store=self.country)
        return_offers = []
        for item in items:
            if 'bucket' in item and item['bucket'] == 'games':  # Only add items that are games and have prices etc.
                return_offers.append(self._item_to_game_offer(item))
        return return_offers

    def get_item_by(self, item_id) -> GameOffer:
        item = _get_item_for_cid(item_id, self.country)
        return self._item_to_game_offer(item)
