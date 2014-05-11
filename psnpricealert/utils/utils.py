import sys
import json

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

def getJsonResponse(url):

    response = urlopen(url)

    enc = response.read().decode('utf-8')
    data = json.loads(enc)

    return data

def prettyPrintJson(jsonString):
    return json.dumps(jsonString, sort_keys=True,indent=4, separators=(',', ': '))

def print_enc(uncoded):
    if version == 2:
        print (uncoded.encode("utf-8"))
    else:
        uncoded = uncoded +"\n"
        sys.stdout.buffer.write(uncoded.encode('utf8'))