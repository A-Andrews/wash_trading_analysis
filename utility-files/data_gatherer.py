import requests
import pandas as pd

url = "https://api.opensea.io/api/v1/assets"

for i in range(0, 4):
    querystring = {"token_ids":list(range((i*50)+1, (i*50)+51)),
                   "asset_contract_address":"0x7Bd29408f11D2bFC23c34f18275bBf23bB716Bc7",
                   "order_direction":"desc",
                   "offset":"0",
                   "limit":"50"}
    response = requests.request("GET", url, params=querystring)
    print(response)