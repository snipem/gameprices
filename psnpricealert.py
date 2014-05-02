import json
import sys
import logging
import argparse
import codecs
import locale

version = sys.version_info[0]

# import only once
if version == 3:
    from urllib.request import urlopen
    from urllib.parse import quote
elif version == 2:
    from urllib2 import urlopen
    from urllib2 import quote
    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
else:
    version == False

logging.basicConfig(
    filename="psnpricealert.log",
    level = logging.DEBUG,
    format = "%(asctime)s [%(levelname)-8s] %(message)s",
    filemode = "w")

parser = argparse.ArgumentParser()
parser.add_argument("--cid", help="CID of game to check")
parser.add_argument("--store", help="regional PSN store to check")
parser.add_argument("--price", help="desired price of game", type=float)

apiRoot = "https://store.sonyentertainmentnetwork.com/store/api/chihiro/00_09_000"

def getJsonResponse(url):
<<<<<<< HEAD

    response = urlopen(url)

    enc = response.read().decode('utf-8')
    data = json.loads(enc)

    return data

def checkWishPrice(cid, store, wishPrice):
    url = apiRoot + "/container/"+store+"/19/"+cid+"?size=99999"
    data = getJsonResponse(url)

    if data == False:
        print("Python 2.x or 3.x required.")
        sys.exit(0)

    print(data['default_sku']['entitlements'][0]['name'] + " - " + data['default_sku']['display_price'])
    currentPrice = float(data['default_sku']['price']) / 100

    if (currentPrice > wishPrice):
        print("Wish price {0:.2f} does not yet match {1:.2f}, exiting".format(wishPrice, currentPrice))
    else:
        print("Wish price %{0:.2f} matched. Is now: %{1:.2f}".format(wishPrice, currentPrice))

    	#TODO send alert
        raise Exception("Alert sending not yet implemented")

def getCidForName(name, store):
    # encode name for HTTP request
    encName = quote(name)

    url = apiRoot+"/bucket_search/"+store+"/19/"+encName+"?size=99999&start=0"
    data = getJsonResponse(url)
    links = data['categories']['games']['links']

    if (len(links) > 1):
        logging.error("Found more than one entry for name " + name)
        for link in links:
            logging.debug ("Found: " + link['default_sku']['entitlements'][0]['name'] + " - " + link['default_sku']['entitlements'][0]['id'])
        raise Exception("More than one entry found for name '" + name + "'. Check log file.")
    else:
        cid = links[0]['default_sku']['entitlements'][0]['id']
        logging.info("Found cid '"+cid+"' for name '"+name+"'")
        return cid

def prettyPrintJson(jsonString):
    print(json.dumps(jsonString, sort_keys=True,indent=4, separators=(',', ': ')))

args = parser.parse_args()
# Read arguments or use example
store = args.store if args.store else "DE/de"
cid = args.cid if args.cid else getCidForName("metal gear solid peace walker psp", store)
wishPrice = args.price if args.price else 15.00
checkWishPrice(cid, store, wishPrice)
