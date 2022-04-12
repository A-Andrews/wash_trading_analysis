import requests
import csv
import sys


opensea_url = "https://api.opensea.io/api/v1/assets"
axie_url = "https://graphql-gateway.axieinfinity.com/graphql"




def get_axie_attributes(ax_id: int):
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

def get_axie_history(ax_id: int):
    payload = {"operationName": "GetAxieTransferHistory","variables": {"axieId": ax_id,"from": 0,"size": 10},
    "query": "query GetAxieTransferHistory($axieId: ID!, $from: Int!, $size: Int!) {axie(axieId: $axieId) {id transferHistory(from: $from, size: $size) {...TransferRecords} ethereumTransferHistory(from: $from, size: $size) {...TransferRecords}}}fragment TransferRecords on TransferRecords {total results {from to timestamp withPrice}}"}
    headers = {"content-type": "application/json"}

    response = requests.request("POST", axie_url, json=payload, headers=headers)
    return response.json()

def write_axie_history_to_row(axie_history):
    data = axie_history["data"]["axie"]
    ax_id, trans_his, eth_trans_his = data["id"], data["transferHistory"], data["ethereumTransferHistory"]
    trans_his_num, trans_his_records = trans_his["total"], trans_his["results"]
    eth_trans_his_num, eth_trans_his_records = eth_trans_his["total"], eth_trans_his["results"]

    trans_list = get_axie_transaction_list(trans_his_num, trans_his_records, ax_id)
    eth_trans_list = get_axie_transaction_list(eth_trans_his_num, eth_trans_his_records, ax_id)

    return trans_list, eth_trans_list


def get_axie_transaction_list(amount, records, ax_id):
    trans_list = []
    for i in range(amount):
        record = records[i]
        rec_from = record["from"]
        rec_to = record["to"]
        price = record["withPrice"]
        time = record["timestamp"]
        trans_list.append([ax_id, rec_to, rec_from, price, time])
    
    return trans_list


def get_csv_axie_transactions(start: int, end: int):

    f = open('../transaction_files/axie_transactions.csv', 'a')
    g = open('../transaction_files/axie_eth_transactions.csv', 'a')

    writer = csv.writer(f)
    eth_writer = csv.writer(g)

    rows = []
    eth_rows = []

    for i in range(start, end):
        data = get_axie_history(i)
        if data == {'message': 'API rate limit exceeded'}:
            print(i)
            break
        try:
            row, eth_row = write_axie_history_to_row(data)
            if row != []: rows.extend(row)
            if eth_row != []: eth_rows.extend(eth_row)
        except:
            print(i)
            
    writer.writerows(rows)
    eth_writer.writerows(eth_rows)

    f.close()
    g.close()




def get_csv_axie(start: int, end: int):

    f = open('../attribute_files/axie_attributes.csv', 'a')

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
        

def main(argv):
    
    start = int(argv[0])
    end = int(argv[1])
    csv = argv[2]

    if start >= end:
        print("Please ensure start is lower than end")
        sys.exit()

    if csv == 'axie':
        get_csv_axie(start, end)

    if csv == 'axie_transactions':
        get_csv_axie_transactions(start, end)

if __name__ == "__main__":
   main(sys.argv[1:])