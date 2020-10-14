import sys
import logging
import time
import datetime
from gameprices.utils import utils

import json
from gameprices.shop import Shop
from gameprices.offer import GameOffer, Price

apiRoot = "https://store.playstation.com/chihiro-api"
storeRoot = "https://store.playstation.com/#!"
fetchSize = "99999"
appendix = ""
apiVersion = "19"

version = sys.version_info[0]

from urllib.request import urlopen
from urllib.parse import quote

""" Dictionary object containing data specific to a Country store. The key is the store identifier per the
PSN API. The array of parameters contains [0]: the country-code folder for the PSN Store URL and
[1]: The currency symbol, in its unicode encoding
[2]: The character preceeding each marketplaces CID """
storeCodeMappings = {
    "NL/nl": ["nl-nl", u'\N{EURO SIGN}'],
    "DE/de": ["de-de", u'\N{EURO SIGN}', "E"],
    "US/en": ["us-en", u'\N{DOLLAR SIGN}', "U"],
    "JP/jp": ["jp-jp", u'\N{YEN SIGN}', "J"]
}


def _filter_none(item):
    if item is None:
        return False
    else:
        return True


def _getItemForCid(cid, store):
    try:
        url = apiRoot + "/viewfinder/" + store + "/" + \
            apiVersion + "/" + cid + "?size=" + fetchSize
        data = utils.get_json_response(url)
        return data
    except Exception as e:
        logging.error("Got error '" + str(e) +
                      "' while retrieving cid '" + cid + "' in store " + store)
        return None


def _get_rewards(item):
    rewards = []

    # TODO Use Default SKU
    #if "default_sku" in item and "rewards" in item["default_sku"]: rewards.append(item["default_sku"]["rewards"].pop())

    for sku in item["skus"]:
        if "rewards" in sku:
            for reward in sku["rewards"]:
                rewards.append(reward)

    return rewards


def _get_display_price(item, store):
    price = _get_price(item)
    displayPrice = storeCodeMappings[store][1] + str(price)

    return displayPrice


def _get_cheapest_price(prices):
    return sorted(filter(_filter_none, prices))[0]


def _get_price(item):
    normalPrice = _get_normal_price(item)
    nonPlaystationPlusPrice = _get_non_playstation_plus_price(item)
    playstationPlusPrice = _get_playstation_plus_price(item)

    return _get_cheapest_price(
        [normalPrice, nonPlaystationPlusPrice, playstationPlusPrice])


def _get_normal_price(item):
    return float(item['default_sku']['price']) / \
        100 if 'default_sku' in item else None


def _get_non_playstation_plus_price(item):
    for reward in _get_rewards(item):
        if (reward.get('reward_type') == 4):
            return float(reward.get('price')) / 100


def _get_playstation_plus_price(item):
    for reward in _get_rewards(item):
        if reward.get('bonus_price') is not None:
            return float(reward.get('bonus_price')) / 100
        elif reward.get('isPlus') is True:
            return float(reward.get('price')) / 100
        else:
            return None

    return None


def _get_name(item):
    return item['name']


def _get_image(item):
    if (len(item["images"]) > 0):
        return item["images"][0]['url']


def _get_offer_end_date(item):
    """ Returns the Offer End Date for a given Item
        :param item: The item for which the Offer End Date is to be retrieved
        :return: A datetime object which is the Offer End Date """

    if item['default_sku'] is not None:
        if 'end_date' in item['default_sku']:
            endDate = item['default_sku']['end_date']
            if endDate is not None:
                return datetime.datetime.strptime(
                    endDate, "%Y-%m-%dT%H:%M:%SZ")


def _get_store_url(item, store):
    cid = item["id"]

    url = storeRoot + "/" + storeCodeMappings[store][0] + "/cid=" + cid

    return url


def _get_cid_for_name(name, store):

    links = _search_for_items_by_name(name, store)
    cids = []

    for link in links:
        try:
            logging.debug("Parsing:\n" + utils.pretty_print_json(link))
            name = link['name']
            itemType = link['default_sku']['name']
            cid = link['id']
            platform = ", ".join(link['playable_platform'])

            logging.info("Found: " + name + " - " + cid +
                         " - Platform: " + platform + " - Type: " + itemType)
            cids.append(cid)
        except Exception as e:
            logging.warning("Got error '" + str(e) +
                         "'' while parsing\n" + utils.pretty_print_json(link))

    return cids


def _search_for_items_by_name(name, store):

    encodedName = quote(name)
    url = apiRoot + "/bucket-search/" + store + "/" + apiVersion + \
        "/" + encodedName + "?size=" + fetchSize + "&start=0"
    data = utils.get_json_response(url)
    links = data['categories']['games']['links']
    return links


def _get_currency_symbol(store):
    try:
        return storeCodeMappings.get(store)[1]
    except:
        return ""


def _determine_store(cid):
    for store in storeCodeMappings:
        storeCodeMapping = storeCodeMappings.get(store)

        if len(storeCodeMapping) >= 3 and cid.startswith(
                storeCodeMappings.get(store)[2]):
            return store


def _get_items_by_container(container, store, filtersDict):

    url = apiRoot + "/viewfinder/" + store + "/" + \
        apiVersion + "/" + container + "?size=" + fetchSize

    for i in filtersDict:
        url = url + "&" + quote(i) + "=" + quote(filtersDict[i])

    data = utils.get_json_response(url)
    links = data['links']

    return links



class Psn(Shop):

    def _build_api_url(self, country, query):
        return "%s/%s/select?q=%s&%s" % (apiRoot, country, query, appendix)

    def _item_to_game_offer(self, game):
        if not game:
            raise Exception("Item is empty")

        return GameOffer(
            id=game["id"],
            cid=game["id"],
            url=game["url"],
            type=game['gameContentTypesList'][0][
                'key'] if 'gameContentTypesList' in game else None,
            name=game["name"],
            # prices=[game['default_sku']['price']/100],
            prices=[
                Price(
                    value=_get_normal_price(game),
                    currency=_get_currency_symbol(self.country),
                    offer_type="NORMAL"
                ),
                Price(
                    value=_get_playstation_plus_price(game),
                    currency=_get_currency_symbol(self.country),
                    offer_type="PS+"
                ),
            ],
            platforms=game['playable_platform'] if 'playable_platform' in game else "",
            picture_url=_get_image(game)
        )

    def search(self, name):
        items = _search_for_items_by_name(name=name, store=self.country)
        return_offers = []
        for item in items:
            return_offers.append(
                self._item_to_game_offer(item)
            )
        return return_offers

    def get_item_by(self, id, name=None):
        item = _getItemForCid(id, self.country)
        return self._item_to_game_offer(item)
