import sys
import urllib.request
import json
from pprint import pprint

from urllib.request import urlopen
from urllib.parse import quote

def get_json_file(filename):
    json_data = open(filename)
    data = json.load(json_data)
    json_data.close()
    return data


def get_json_response(url):

    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())


def pretty_print_json(jsonString):
    return json.dumps(
        jsonString,
        sort_keys=True,
        indent=4,
        separators=(
            ',',
            ': '))


def print_enc(s):
    print(s.decode('utf-8') if isinstance(s, type(b'')) else s)
