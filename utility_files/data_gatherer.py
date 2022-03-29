import requests
import pandas as pd
import csv
import json
import sys
import getopt

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

# id,class,genes,breedCount,level,hp,speed,skill,morale,eyes,ears,back,mouth,horn,tail,ability1,ability2,ability3,ability4


opensea_url = "https://api.opensea.io/api/v1/assets"
axie_url = "https://graphql-gateway.axieinfinity.com/graphql"




def get_axie_attributes(ax_id: int):
    axie_id = str(ax_id)
    payload = {
                "operation": "GetAxieDetail",
                "variables": {"axieId": ax_id},
                "query": "query GetAxieDetail($axieId: ID!) {axie(axieId: $axieId) {...AxieDetail}}fragment AxieDetail on Axie {id class genes class breedCount level parts { ...AxiePart} stats { ...AxieStats}} fragment AxiePart on AxiePart {class type specialGenes abilities {...AxieCardAbility}} fragment AxieCardAbility on AxieCardAbility {id name attack defense energy} fragment AxieStats on AxieStats {hp speed skill morale}"}
    headers = {"content-type": "application/json"}

    response = requests.request("POST", axie_url, json=payload, headers=headers)
    return response.json()

def write_axie_to_row(axie):

    data = axie["data"]["axie"]
    ax_id, ax_class, genes, breedCount, level = data["id"], data["class"], data["genes"], data["breedCount"], data["level"]
    stats = data["stats"]
    hp, speed, skill, morale = stats["hp"], stats["speed"], stats["skill"], stats["morale"]
    parts = data["parts"]
    eyes, ears, back, mouth, horn, tail = parts[0]["class"], parts[1]["class"], parts[2]["class"], parts[3]["class"], parts[4]["class"], parts[5]["class"]
    ability1, ability2, ability3, ability4 = parts[2]["abilities"][0]["name"], parts[3]["abilities"][0]["name"], parts[4]["abilities"][0]["name"], parts[5]["abilities"][0]["name"]

    return [ax_id,ax_class,genes,breedCount,level,hp,speed,skill,morale,eyes,ears,back,mouth,horn,tail,ability1,ability2,ability3,ability4]


def get_csv_axie(start: int, end: int):

    f = open('attribute_files/axie_attributes.csv', 'a')

    writer = csv.writer(f)

    rows = []

    for i in range(start, end):
        data = get_axie_attributes(i)
        try:
            row = write_axie_to_row(data)
            rows.append(row)
        except:
            print(i)
        
    writer.writerows(rows)
        
    

    f.close()
        

#get_csv_axie(1000, 11000)

def main(argv):
    
    start = int(argv[0])
    end = int(argv[1])
    csv = argv[2]

    if start >= end:
        print("Please ensure start is lower than end")
        sys.exit()

    if csv == 'axie':
        get_csv_axie(start, end)

if __name__ == "__main__":
   main(sys.argv[1:])