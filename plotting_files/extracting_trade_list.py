import pandas as pd
import numpy as np

# given a series name returns their data, the list of id numbers and the list of unique buyers
def get_opensea_trade_data(series):
    data = pd.read_csv(f"transaction_files/{series}_transfers.csv")
    ids = data[['id']].copy()
    ids = ids['id'].unique()
    addresses = data[['buyer_address']].copy()
    addresses = addresses['buyer_address'].unique()

    return data, ids, addresses
    
# given an id and the data returns a list of wallets that have held that id and at what times they were
def get_opensea_addresses_times(data, i):
    rows = data.loc[data["id"] == i]
    wallets = rows[['buyer_address']].to_numpy()
    times = rows[['time']].to_numpy()

    return wallets, times

# given data and a list of ids returns the address lists and time lists associated with those ids
def get_all_address_time_pairs(data, ids):
    address_list = []
    times_list = []
    for i in ids:
        wallets, times = get_opensea_addresses_times(data, i)
        address_list.append(wallets)
        times_list.append(times)

    return address_list, times_list

# given data and an address return a list of addresses it has sent to and a list of a addresses it has recieved from
def get_to_from_addresses(data, address):
    to_rows = data.loc[data['seller_address'] == address]
    to_addresses = to_rows[['buyer_address']].to_numpy()

    from_rows = data.loc[data['buyer_address'] == address]
    from_addresses = from_rows[['seller_address']].to_numpy()

    return to_addresses, from_addresses

# given the data and a list of addresses returns the lists of sent to and recieved from addresses for each one
def get_all_to_from(data, addresses):
    to_list = []
    from_list = []

    for i in addresses.index:
        to_addresses, from_addresses = get_to_from_addresses(data, i)
        to_list.append(to_addresses)
        from_list.append(from_addresses)

    return to_list, from_list

# given data and minimum number of interactions return buyer addresses that meet or exceed that minimum
def get_common_addresses(data, min_count):
    counts = data['buyer_address'].value_counts()
    return counts.loc[counts >= min_count].sort_values(ascending = False)

# given data and a minimum number of exchanges find pairs that occur atleast that many times
def get_common_pairs(data, min_count):
    data_addresses = data[['seller_address', 'buyer_address']]
    counts = data_addresses.groupby(['seller_address', 'buyer_address']).value_counts()
    return counts.loc[counts >= min_count].sort_values(ascending = False)

# given a list of common pairs or addresses returns the top x of that
def get_topx_common(common, amount):
    return common.head(amount)

# given a df of pairs of addresses returns them as a list of node to node pairs
def get_node_pairs_from_pairs(addresses):
    return addresses.index.tolist()

# Given list of addresses returns list of pairs of those addresses connections as node to node pairs
def get_node_pairs_from_singles(data, addresses, duplicates = False):
    out = []
    to_list, from_list = get_all_to_from(data, addresses)
    for i in range(0, len(to_list)):
        node_to_list = map(lambda e: (addresses.index[i], e[0]), to_list[i])
        node_from_list = map(lambda e: (e[0], addresses.index[i]), from_list[i])
        out.extend(node_to_list)
        out.extend(node_from_list)
    if duplicates:
        return out

    return list(dict.fromkeys(out))

# helper function for find_loops
def indices(lst, item):
    return [i for i, x in enumerate(lst) if x == item]

# given list of addresses checks for loops returns a list of addreses in the loop(s) if a loop is not present returns an empty list
def find_loops(addresses):

    if len(addresses) == len(set(addresses)): return []

    out = []

    for i, address in enumerate(addresses):
        indexes = indices(addresses, address)
        if len(indexes) > 1:
            for j in indexes:
                if j > i:
                    out.append(addresses[i:j+1])

    return out

def flatten(t):
    return [item for sublist in t for item in sublist]

# given list of ids finds series of common addresses of x length that occur y number of times
def find_common_sequences(data, ids, min_length = 1, min_occurances = 1):

    address_list, _ = get_all_address_time_pairs(data, ids)

    min_length_lists = [i for i in address_list if len(i) >= min_length]
    counts = {}
    for i in min_length_lists:
        if len(i) == min_length:
            key = ','.join(flatten(i.tolist()))
            counts[key] = counts.get(key, 0) + 1

        else:
            keys = map(list, zip(*(flatten(i.tolist())[j:] for j in range(min_length))))
            for k in keys:
                key = ','.join(k)
                counts[key] = counts.get(key, 0) + 1

    out = [k.split(',') for k, v in counts.items() if v >= min_occurances]

    return out

# given list of ids finds sequences containing x number of related addresses that occur together y number of times
def find_associated_addresses(data, ids, min_length = 1, min_occurances = 1):
    address_list, _ = get_all_address_time_pairs(data, ids)

    min_length_lists = [list(set(flatten(i.tolist()))) for i in address_list if len(list(set(flatten(i.tolist())))) >= min_length]
    counts = {}
    for i in min_length_lists:
        if len(i) == min_length:
            key = frozenset(i)
            counts[key] = counts.get(key, 0) + 1

        else:
            keys = map(list, zip(*(i[j:] for j in range(min_length))))
            for k in keys:
                key = frozenset(k)
                counts[key] = counts.get(key, 0) + 1

    out = [list(k) for k, v in counts.items() if v >= min_occurances]
    return out

def create_adjacency_matrix():
    # Creates adjacency matrix given list of pairs
    return 0


data, ids, addresses = get_opensea_trade_data('BAYC')
#common_adds = get_common_addresses(data, 9)
#print(common_adds)
#test = get_node_pairs_from_singles(data, common_adds)
#print(test)
#print(len(test))

#print(find_loops([4,3,5,4,6,4,6,3,4]))
#cs = find_common_sequences(data, ids, 7, 7)
#print(cs)
#print(len(cs))

cs = find_associated_addresses(data, ids, 7, 7)
print(cs)
print(len(cs))
