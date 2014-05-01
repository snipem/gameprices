import json
import sys
import logging

logging.basicConfig( 
    filename="psnpricealert.log", 
    level = logging.DEBUG, 
    format = "%(asctime)s [%(levelname)-8s] %(message)s",
    filemode = "w")

apiRoot = "https://store.sonyentertainmentnetwork.com/store/api/chihiro/00_09_000"

def getJsonResponse(url):
    # Python 2.x or 3.x support
    version = sys.version_info[0]
    if version == 3:
        from urllib.request import urlopen
    elif version == 2:
        import urllib

    if version == 3:
        response = urlopen(url)
        enc = response.read().decode('utf-8')
        data = json.loads(enc)
    elif version == 2:
        response = urllib.urlopen(url)
        data = json.load(response)
        return data

def checkWishPrice(cid, store, wishPrice):

    url = apiRoot + "/container/"+store+"/19/"+cid+"?size=99999"

    data = getJsonResponse(url)
    print(data['default_sku']['entitlements'][0]['name'].encode("utf-8") + " - " + data['default_sku']['display_price'].encode("utf-8"))  

    currentPrice = float(data['default_sku']['price']) / 100

    if (currentPrice > wishPrice):
    	print "Wish price %.2f not yet matched %.2f, exiting" %(wishPrice, currentPrice)
    else:
    	print "Wish price %.2f matched. Is now: %.2f" %(wishPrice, currentPrice)
    	#TODO send alert
        raise Exception("Alert sending not yet implemented")

def getCidForName(name, store):

    url = apiRoot+"/bucket_search/"+store+"/19/"+name+"?size=99999&start=0"
    data = getJsonResponse(url)

    links = data['categories']['games']['links']

    if (len(links) > 1):
        logging.error("Found more than one entry for name " + name)
        for link in links:
            logging.debug ("Found: " + link['default_sku']['entitlements'][0]['name'] + " - " + link['default_sku']['entitlements'][0]['id'])
        raise Exception("More than one entry found for name '" + name + "'")
    else:
        cid = links[0]['default_sku']['entitlements'][0]['id']
        logging.info("Found cid '"+cid+"' for name '"+name+"'")
        return cid

def prettyPrintJson(jsonString):
    print(json.dumps(jsonString, sort_keys=True,indent=4, separators=(',', ': ')))

#Example
store = "DE/de"
cid = getCidForName("metal gear solid peace walker psp", store)
wishPrice = 15.00
checkWishPrice(cid, store, wishPrice)
