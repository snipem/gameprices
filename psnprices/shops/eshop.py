import requests
import json
from psnprices.shop import Shop
from psnprices.offer import GameOffer

apiRoot = ""
storeRoot = ""
fetchSize = ""
apiVersion = ""
country = "de"

class Eshop(Shop):

    def _build_api_url(self, country, query):
        return "%s/%s/select?q=%s&%s" % (apiRoot, country, query, appendix)

    def search(self, name):
        url = ""
        r = requests.get(url)
        payload = json.loads(r.text)

        return_offers = []

        for group in payload['grouped']['pg_s']['groups']:
            if group['groupValue'] == "GAME":
                for game in group['doclist']['docs']:
                    return_offers.append(
                        GameOffer(
                            id=game["fs_id"],
                            url=game["url"],
                            name=game["title"],
                            prices=[game['price_lowest_f']],
                            platforms=game['system_names_txt'],
                            picture_url=game['image_url']
                            )
                        )

        return return_offers

    def get_item_by(self, id, name):
        game_offers = self.search(name)
        for game_offer in game_offers:
            if game_offer.id == id:
                return game_offer
