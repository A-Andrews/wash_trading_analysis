import requests
import pandas as pd

#{
#  "operation": "GetAxieDetail",
#  "variables": {
#    "axieId": "940499"
#  },
#  "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
#}

#querystring = {"token_ids":list(range((i*50)+1, (i*50)+51)),
#                   "asset_contract_address":"0x7Bd29408f11D2bFC23c34f18275bBf23bB716Bc7",
#                   "order_direction":"desc",
#                   "offset":"0",
#                   "limit":"50"}

opensea_url = "https://api.opensea.io/api/v1/assets"
axie_url = "https://graphql-gateway.axieinfinity.com/graphql"




def get_axie_attributes(id: int):
    axie_id = str(id)
    payload = {
                "operation": "GetAxieDetail",
                "variables": {"axieId": "1000"},
                "query": "query GetAxieDetail($axieId: ID!) {axie(axieId: $axieId) {...AxieDetail}}fragment AxieDetail on Axie {id class name genes birthDate bodyShape class stage breedCount level parts { ...AxiePart} stats { ...AxieStats}} fragment AxiePart on AxiePart {id name class type specialGenes stage abilities {...AxieCardAbility}} fragment AxieCardAbility on AxieCardAbility {id name attack defense energy} fragment AxieStats on AxieStats {hp speed skill morale}"}
    headers = {"content-type": "application/json"}

    response = requests.request("POST", axie_url, json=payload, headers=headers)
    return response.json

