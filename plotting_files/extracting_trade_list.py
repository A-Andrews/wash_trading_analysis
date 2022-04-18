import pandas as pd
import numpy as np

def get_opensea_trade_data(series):
    data = pd.read_csv(f"transaction_files/{series}_transfers.csv")
    ids = data[['id']].copy()
    ids = ids['id'].unique()
    addresses = data[['buyer_address']].copy()
    addresses = addresses['buyer_address'].unique()

    return data, ids, addresses
    
def get_opensea_addresses_times(data, i):
    rows = data.loc[data["id"] == i]
    wallets = rows[['buyer_address']].to_numpy()
    times = rows[['time']].to_numpy()

    return wallets, times
        
def get_all_address_time_pairs(data, ids):
    address_list = []
    times_list = []
    for i in ids:
        wallets, times = get_opensea_addresses_times(data, i)
        address_list.append(wallets)
        times_list.append(times)

    return address_list, times_list

def get_to_from_addresses(data, address):
    to_rows = data.loc[data['seller_address'] == address]
    to_addresses = to_rows[['buyer_address']].to_numpy()

    from_rows = data.loc[data['buyer_address'] == address]
    from_addresses = from_rows[['seller_address']].to_numpy()

    return to_addresses, from_addresses

def get_all_to_from(data, addresses):
    to_list = []
    from_list = []

    for i in addresses:
        to_addresses, from_addresses = get_to_from_addresses(data, i)
        to_list.append(to_addresses)
        from_list.append(from_addresses)

    return to_list, from_list

def get_common_addresses(data, min_count):
    counts = data['buyer_address'].value_counts()
    return counts.loc[counts >= min_count]

def get_common_pairs(data, min_count):
    data_addresses = data[['seller_address', 'buyer_address']]
    counts = data_addresses.groupby(['seller_address', 'buyer_address']).value_counts()
    return counts.loc[counts >= min_count]

data, ids, addresses = get_opensea_trade_data('BAYC')
print(get_common_pairs(data, 9))
