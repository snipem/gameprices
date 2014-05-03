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
else:
    version == False

logging.basicConfig(
    filename="psnpricealert.log",
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)-8s] %(message)s",
    filemode = "w")

parser = argparse.ArgumentParser()
parser.add_argument("--cid", help="CID of game to check")
parser.add_argument("--store", help="regional PSN store to check")
parser.add_argument("--price", help="desired price of game", type=float)
parser.add_argument("--search", help="Name of item to search for")

apiRoot = "https://store.sonyentertainmentnetwork.com/store/api/chihiro/00_09_000"

def getJsonResponse(url):

    response = urlopen(url)

    enc = response.read().decode('utf-8')
    data = json.loads(enc)

    return data

def checkWishPrice(cid, store, wishPrice):
    url = apiRoot + "/container/"+store+"/19/"+cid+"?size=99999"
    data = getJsonResponse(url)

    print_enc(data['default_sku']['entitlements'][0]['name'] + " - " + data['default_sku']['display_price'])
    currentPrice = float(data['default_sku']['price']) / 100

    if (currentPrice > wishPrice):
        print_enc("Wish price {0:.2f} does not yet match {1:.2f}, exiting".format(wishPrice, currentPrice))
        return False
    else:
        print_enc("Wish price %{0:.2f} matched. Is now: %{1:.2f}".format(wishPrice, currentPrice))
        return True

def getCidForName(name, store):
    # encode name for HTTP request
    encName = quote(name)

    url = apiRoot+"/bucket_search/"+store+"/19/"+encName+"?size=99999&start=0"
    data = getJsonResponse(url)
    links = data['categories']['games']['links']
    cids = []


    for link in links:
        try:
            logging.debug("Parsing:\n" + prettyPrintJson(link))
            name = link['name']
            itemType = link['default_sku']['name']
            cid = link['default_sku']['entitlements'][0]['id']
            platform = link['playable_platform']
        
            logging.info ("Found: " + name + " - " + cid + " - Platform: " + str(platform) + " - Type: " + itemType)
            cids.append(cid)
        except Exception , e:
            logging.warn("Got error '"+e+"'' while parsing\n" + prettyPrintJson(link))

    return cids

def prettyPrintJson(jsonString):
    return json.dumps(jsonString, sort_keys=True,indent=4, separators=(',', ': '))

def print_enc(uncoded):
    if version == 2:
        print (uncoded.encode("utf-8"))
    else:
        uncoded = uncoded +"\n"
        sys.stdout.buffer.write(uncoded.encode('utf8'))

def main():
    args = parser.parse_args()

    if (args.search != None and args.store != None):
        cids = getCidForName(args.search,args.store)

        if (len(cids) != 1):
            logging.error("Found "+str(len(cids))+" entries for name '" + args.search + "' while searching for only one")
            exit(-1)
        else:
            print (cids.pop())
            exit(0)

    elif (args.store != None and args.cid != None and args.price != None):
        priceMatched = checkWishPrice(args.cid, args.store, args.price)
        if (priceMatched):
            exit(0)
        else:
            exit(-1)

if __name__ == "__main__":
    main()
