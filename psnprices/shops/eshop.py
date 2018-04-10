import requests
import json
from psnprices.shop import Shop
from psnprices.offer import GameOffer, Price

apiRoot = ""
storeRoot = ""
fetchSize = ""
apiVersion = ""
country = "de"
limit = 30

class Eshop(Shop):

    def _build_api_url(self, country, query):
        return "%s/%s/select?q=%s&%s" % (apiRoot, country, query, appendix)

    def search(self, name):
        url = "https://search.nintendo-europe.com/"+country+"/select?q="+name+"&fq=type%3A*%20AND%20*%3A*&start=0&rows=24&wt=json&group=true&group.field=pg_s&group.limit="+str(limit)+"&group.sort=score%20desc,%20date_from%20desc&sort=score%20desc,%20date_from%20desc"
        r = requests.get(url)
        payload = json.loads(r.text)

        return_offers = []

        for group in payload['grouped']['pg_s']['groups']:
            if group['groupValue'] == "GAME":
                for game in group['doclist']['docs']:
                    price = game['price_lowest_f']
                    return_offers.append(
                        GameOffer(
                            id=game["fs_id"],
                            url=game["url"],
                            name=game["title"],
                            type=game["type"],
                            prices=[
                                Price(
                                    value=price if price > 0 else None,
                                    #TODO add currency
                                    currency="",
                                    offer_type="LOWEST"
                                    ),
                            ],
                            platforms=game['system_names_txt'],
                            picture_url=game['image_url'] if 'image_url' in game else None
                            )
                        )

        return return_offers