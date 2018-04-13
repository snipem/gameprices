import sys
import logging
import time
import datetime
from pprint import pprint
from psnprices.utils import utils

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
    "DE/de": ["de-de", u'\N{EURO SIGN}',"E"],
    "US/en": ["us-en", u'\N{DOLLAR SIGN}',"U"],
    "JP/jp": ["jp-jp", u'\N{YEN SIGN}',"J"]
}


def _filterNone(item):
    if item is None:
        return False
    else:
        return True


def _getItemForCid(cid, store):
    try:
        url = apiRoot + "/viewfinder/" + store + "/" + \
            apiVersion + "/" + cid + "?size=" + fetchSize
        data = utils.getJsonResponse(url)
        return data
    except Exception as e:
        logging.error("Got error '" + str(e) +
                      "' while retrieving cid '" + cid + "' in store " + store)
        return None


def _getRewards(item):
    rewards = []

    # TODO Use Default SKU
    #if "default_sku" in item and "rewards" in item["default_sku"]: rewards.append(item["default_sku"]["rewards"].pop())

    for sku in item["skus"]:
        if "rewards" in sku:
            for reward in sku["rewards"]:
                rewards.append(reward)

    return rewards


def _getDisplayPrice(item, store):
    price = _getPrice(item)
    displayPrice = storeCodeMappings[store][1] + str(price)

    return displayPrice


def _getCheapestPrice(prices):
    return sorted(filter(_filterNone, prices))[0]


def _getPrice(item):
    normalPrice = _getNormalPrice(item)
    nonPlaystationPlusPrice = _getNonPlaystationPlusPrice(item)
    playstationPlusPrice = _getPlaystationPlusPrice(item)

    return _getCheapestPrice([normalPrice, nonPlaystationPlusPrice, playstationPlusPrice])


def _getNormalPrice(item):
    return float(item['default_sku']['price']) / 100 if 'default_sku' in item else None


def _getNonPlaystationPlusPrice(item):
    for reward in _getRewards(item):
        if (reward.get('reward_type') == 4):
            return float(reward.get('price')) / 100


def _getPlaystationPlusPrice(item):
    for reward in _getRewards(item):
        if reward.get('bonus_price') is not None:
            return float(reward.get('bonus_price')) / 100
        elif reward.get('isPlus') is True:
            return float(reward.get('price')) / 100
        else:
            return None

    return None


def _getName(item):
    return item['name']


def _getImage(item):
    if (len(item["images"]) > 0):
        return item["images"][0]['url']


def _getOfferEndDate(item):
    """ Returns the Offer End Date for a given Item
        :param item: The item for which the Offer End Date is to be retrieved
        :return: A datetime object which is the Offer End Date """

    if item['default_sku'] is not None:
        if 'end_date' in item['default_sku']:
            endDate = item['default_sku']['end_date']
            if endDate is not None:
                return datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%SZ")


def _getStoreUrl(item, store):
    cid = item["id"]

    url = storeRoot + "/" + storeCodeMappings[store][0] + "/cid=" + cid

    return url


def _getCidForName(name, store):

    links = _searchForItemsByName(name, store)
    cids = []

    for link in links:
        try:
            logging.debug("Parsing:\n" + utils.prettyPrintJson(link))
            name = link['name']
            itemType = link['default_sku']['name']
            cid = link['id']
            platform = ", ".join(link['playable_platform'])

            logging.info("Found: " + name + " - " + cid +
                         " - Platform: " + platform + " - Type: " + itemType)
            cids.append(cid)
        except Exception as e:
            logging.warn("Got error '" + str(e) +
                         "'' while parsing\n" + utils.prettyPrintJson(link))

    return cids


def _searchForItemsByName(name, store):

    encodedName = quote(name)
    url = apiRoot + "/bucket-search/" + store + "/" + apiVersion + \
        "/" + encodedName + "?size=" + fetchSize + "&start=0"
    data = utils.getJsonResponse(url)
    links = data['categories']['games']['links']
    return links

def _getCurrencySymbol(store):
    try:
        return storeCodeMappings.get(store)[1] 
    except:
        return ""

def _determineStore(cid):
    for store in storeCodeMappings:
        storeCodeMapping = storeCodeMappings.get(store)
         
        if len(storeCodeMapping) >= 3 and cid.startswith(storeCodeMappings.get(store)[2]):
            return store 

def _getItemsByContainer(container, store, filtersDict):

    encContainer = quote(container)
    timestamp = timestamp = int(time.time())

    url = apiRoot + "/viewfinder/" + store + "/" + \
        apiVersion + "/" + container + "?size=" + fetchSize

    for i in filtersDict:
        url = url + "&" + quote(i) + "=" + quote(filtersDict[i])

    data = utils.getJsonResponse(url)
    links = data['links']

    return links


import requests
import json
from psnprices.shop import Shop
from psnprices.offer import GameOffer, Price

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
                    type=game['gameContentTypesList'][0]['key'] if 'gameContentTypesList' in game else None,
                    name=game["name"],
                    # prices=[game['default_sku']['price']/100],
                    prices=[
                        Price(
                            value=_getNormalPrice(game),
                            currency=_getCurrencySymbol(self.country),
                            offer_type="NORMAL"
                            ),
                        Price(
                            value=_getPlaystationPlusPrice(game),
                            currency=_getCurrencySymbol(self.country),
                            offer_type="PS+"
                            ),
                    ],
                    platforms=game['playable_platform'],
                    picture_url=_getImage(game)
                    )

    def search(self, name):
        items = _searchForItemsByName(name=name, store=self.country)
        return_offers=[]
        for item in items:
            return_offers.append(
                        self._item_to_game_offer(item)
                        )
        return return_offers

    def get_item_by(self, id, name=None):
        item = _getItemForCid(id, self.country)
        return self._item_to_game_offer(item)


