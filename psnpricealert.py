import json
import sys
# Python 2.x or 3.x support
version = sys.version_info[0]
if version == 3:
    from urllib.request import urlopen
elif version == 2:
    import urllib

#Example
lang = "DE/de"
#cid must be extracted from the browser view
cid = "EP0101-ULES01372_00-GPCMETALGE000001"
wishprice = 15.00

url = "https://store.sonyentertainmentnetwork.com/store/api/chihiro/00_09_000/container/"+lang+"/19/"+cid+"?size=99999"

if version == 3:
    response = urlopen(url)
    enc = response.read().decode('utf-8')
    data = json.loads(enc)
    print(data['default_sku']['entitlements'][0]['name'],' - ',data['default_sku']['display_price'])
elif version == 2:
    response = urllib2.urlopen(url)
    data = json.load(response)
    print(data['default_sku']['entitlements'][0]['name'].encode("utf-8") + " - " + data['default_sku']['display_price'].encode("utf-8"))  

print data['default_sku']['entitlements'][0]['name'].encode("utf-8") + " - " + data['default_sku']['display_price'].encode("utf8")

currentPrice = float(data['default_sku']['price']) / 100

if (currentPrice > wishprice):
	print "Wish price %.2f not yet matched %.2f, exiting" %(wishprice, currentPrice)
else:
	print "Wish price %.2f matched. Is now: %.2f" %(wishprice, currentPrice)
	#TODO send alert
