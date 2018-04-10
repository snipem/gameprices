import sys
import logging
import time
import datetime
from pprint import pprint
from psnprices.utils import utils

apiRoot = "https://store.playstation.com/chihiro-api"
storeRoot = "https://store.playstation.com/#!"
fetchSize = "99999"
apiVersion = "19"

version = sys.version_info[0]

# import only once
if version == 3:
    from urllib.request import urlopen
    from urllib.parse import quote
elif version == 2:
    from urllib2 import urlopen
    from urllib2 import quote
else:
    version == False

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


def filterNone(item):
    if item is None:
        return False
    else:
        return True


def getItemForCid(cid, store):
    try:
        url = apiRoot + "/viewfinder/" + store + "/" + \
            apiVersion + "/" + cid + "?size=" + fetchSize
        data = utils.getJsonResponse(url)
        return data
    except Exception as e:
        logging.error("Got error '" + str(e) +
                      "' while retrieving cid '" + cid + "' in store " + store)
        return None


def getRewards(item):
    rewards = []

    # TODO Use Default SKU
    #if "default_sku" in item and "rewards" in item["default_sku"]: rewards.append(item["default_sku"]["rewards"].pop())

    for sku in item["skus"]:
        if "rewards" in sku:
            for reward in sku["rewards"]:
                rewards.append(reward)

    return rewards


def getDisplayPrice(item, store):
    price = getPrice(item)
    displayPrice = storeCodeMappings[store][1] + str(price)

    return displayPrice


def getCheapestPrice(prices):
    return sorted(filter(filterNone, prices))[0]


def getPrice(item):
    normalPrice = getNormalPrice(item)
    nonPlaystationPlusPrice = getNonPlaystationPlusPrice(item)
    playstationPlusPrice = getPlaystationPlusPrice(item)

    return getCheapestPrice([normalPrice, nonPlaystationPlusPrice, playstationPlusPrice])


def getNormalPrice(item):
    return float(item['default_sku']['price']) / 100 if 'default_sku' in item else None


def getNonPlaystationPlusPrice(item):
    for reward in getRewards(item):
        if (reward.get('reward_type') == 4):
            return float(reward.get('price')) / 100


def getPlaystationPlusPrice(item):
    for reward in getRewards(item):
        if reward.get('bonus_price') is not None:
            return float(reward.get('bonus_price')) / 100
        elif reward.get('isPlus') is True:
            return float(reward.get('price')) / 100
        else:
            return None

    return None


def getName(item):
    return item['name']


def getImage(item):
    if (len(item["images"]) > 0):
        return item["images"][0]['url']


def getOfferEndDate(item):
    """ Returns the Offer End Date for a given Item
        :param item: The item for which the Offer End Date is to be retrieved
        :return: A datetime object which is the Offer End Date """

    if item['default_sku'] is not None:
        if 'end_date' in item['default_sku']:
            endDate = item['default_sku']['end_date']
            if endDate is not None:
                return datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%SZ")


def getStoreUrl(item, store):
    cid = item["id"]

    url = storeRoot + "/" + storeCodeMappings[store][0] + "/cid=" + cid

    return url


def getCidForName(name, store):

    links = searchForItemsByName(name, store)
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


def searchForItemsByName(name, store):

    encodedName = quote(name)
    url = apiRoot + "/bucket-search/" + store + "/" + apiVersion + \
        "/" + encodedName + "?size=" + fetchSize + "&start=0"
    data = utils.getJsonResponse(url)
    links = data['categories']['games']['links']
    return links

def getCurrencySymbol(store):
    try:
        return storeCodeMappings.get(store)[1] 
    except:
        return ""

def determineStore(cid):
    for store in storeCodeMappings:
        storeCodeMapping = storeCodeMappings.get(store)
         
        if len(storeCodeMapping) >= 3 and cid.startswith(storeCodeMappings.get(store)[2]):
            return store 

def getItemsByContainer(container, store, filtersDict):

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
        return GameOffer(
                    id=game["id"],
                    url=game["url"],
                    type=game['gameContentTypesList'][0]['key'] if 'gameContentTypesList' in game else None,
                    name=game["name"],
                    # prices=[game['default_sku']['price']/100],
                    prices=[
                        Price(
                            value=getNormalPrice(game),
                            currency=getCurrencySymbol(self.country),
                            offer_type="NORMAL"
                            ),
                        Price(
                            value=getPlaystationPlusPrice(game),
                            currency=getCurrencySymbol(self.country),
                            offer_type="PS+"
                            ),
                    ],
                    platforms=game['playable_platform'],
                    picture_url=getImage(game)
                    )


    def search(self, name):
        items = searchForItemsByName(name=name, store=self.country)
        return_offers=[]
        for item in items:
            return_offers.append(
                        self._item_to_game_offer(item)
                        )
        return return_offers

    def get_item_by(self, id, name):
        item = getItemForCid(id, self.country)
        return self._item_to_game_offer(item)


