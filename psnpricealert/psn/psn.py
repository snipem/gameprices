import sys
import logging
from psnpricealert.utils import utils
import time

apiRoot = "https://store.playstation.com/chihiro-api"
storeRoot = "https://store.playstation.com/#!"
fetchSize = "99999"
apiVersion = "19"

version = sys.version_info[0]

logging.basicConfig(
    filename="log/psn.log",
    level = logging.DEBUG,
    format = "%(asctime)s [%(levelname)-8s] %(message)s",
    filemode = "w")

# import only once
if version == 3:
    from urllib.request import urlopen
    from urllib.parse import quote
elif version == 2:
    from urllib2 import urlopen
    from urllib2 import quote
else:
    version == False


storeCodeMappings = {
    "NL/nl": "nl-nl"
}

def getItemForCid(cid, store):
    try:
        url = apiRoot + "/viewfinder/"+store+"/"+apiVersion+"/"+cid+"?size="+fetchSize
        data = utils.getJsonResponse(url)
        return data
    except Exception as e:
        logging.error("Got error '"+str(e)+"' while retrieving cid '"+cid+"' in store "+store)
        return None

def getPrice(item):
    return getPlaystationPlusPrice(item)

def getNormalPrice(item):
    return float(item['default_sku']['price'])/100

def getPlaystationPlusPrice(item):
    rewards = item['default_sku']['rewards']
    for reward in rewards:
        if (reward['reward_type'] == 2 and reward['isPlus']):
            return float(reward['price'])/100

    return getNormalPrice(item)
 
def getName(item):
    return item['name']

def getImage(item):
    if (len (item["images"]) > 0):
        return item["images"][0]['url']

def getStoreUrl(item, store):
    cid = item["id"]

    url = storeRoot + "/" + storeCodeMappings[store] + "/cid=" + cid

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
        
            logging.info ("Found: " + name + " - " + cid + " - Platform: " + platform + " - Type: " + itemType)
            cids.append(cid)
        except Exception as e:
            logging.warn("Got error '"+str(e)+"'' while parsing\n" + utils.prettyPrintJson(link))

    return cids

def searchForItemsByName(name, store):

    encodedName = quote(name)
    url = apiRoot+"/bucket-search/"+store+"/"+apiVersion+"/"+encodedName+"?size="+fetchSize+"&start=0"
    data = utils.getJsonResponse(url)
    links = data['categories']['games']['links']
    return links

def getItemsByContainer(container, store, filtersDict):

    encContainer = quote(container)
    timestamp = timestamp = int(time.time())

    url = apiRoot+"/viewfinder/"+store+"/"+apiVersion+"/"+container+"?size="+fetchSize

    for i in filtersDict:
        url = url + "&" + quote(i) + "=" + quote(filtersDict[i])

    data = utils.getJsonResponse(url)
    links = data['links']

    return links
