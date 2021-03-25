import json
import urllib.request


def get_json_file(filename):
    json_data = open(filename)
    data = json.load(json_data)
    json_data.close()
    return data


def get_json_response(url):

    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())


def pretty_print_json(json_string):
    return json.dumps(json_string, sort_keys=True, indent=4, separators=(",", ": "))


def print_enc(s):
    print(s.decode("utf-8") if isinstance(s, type(b"")) else s)
