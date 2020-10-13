import urllib.request
import json
from gameprices.shop import Shop
from gameprices.offer import GameOffer, Price
from gameprices.utils import utils

apiRoot = ""
storeRoot = ""
fetchSize = ""
apiVersion = ""
country = "de"
appendix = ""
limit = 30


class Eshop(Shop):

    whitespace_replacer = "_"
    id_spacer = "###"

    def _build_api_url(self, country, query):
        return "%s/%s/select?q=%s&%s" % (apiRoot, country, query, appendix)

    def _encode_id(self, id, name):
        return self.country + self.id_spacer + \
            str(id) + self.id_spacer + name.replace(" ", self.whitespace_replacer)

    def _decode_id(self, encoded_id):
        split_id = encoded_id.split(self.id_spacer)
        country = split_id[0]
        id = split_id[1]
        name = split_id[2].replace(self.whitespace_replacer, " ")
        return country, id, name

    def search(self, name):
        url = "https://search.nintendo-europe.com/" + country + "/select?q=" + urllib.parse.quote(name) + "&fq=type%3A*%20AND%20*%3A*&start=0&rows=24&wt=json&group=true&group.field=pg_s&group.limit=" + \
            str(limit) + "&group.sort=score%20desc,%20date_from%20desc&sort=score%20desc,%20date_from%20desc"

        payload = utils.get_json_response(url)

        return_offers = []

        for group in payload['grouped']['pg_s']['groups']:
            if group['groupValue'] == "GAME":
                for game in group['doclist']['docs']:
                    price = game['price_lowest_f']
                    return_offers.append(
                        GameOffer(
                            id=game["fs_id"],
                            cid=self._encode_id(
                                id=game["fs_id"], name=game["title"]),
                            url=game["url"],
                            name=game["title"],
                            type=game["type"],
                            prices=[
                                Price(
                                    value=price if price > 0 else None,
                                    # TODO add currency
                                    currency="",
                                    offer_type="LOWEST"
                                ),
                            ],
                            platforms=game['system_names_txt'],
                            picture_url=game[
                                'image_url'] if 'image_url' in game else None
                        )
                    )

        return return_offers

    def get_item_by(self, id, name=None):
        country, id, name = self._decode_id(id)
        games = self.search(name=name)
        for game in games:
            if game.id == id:
                return game
