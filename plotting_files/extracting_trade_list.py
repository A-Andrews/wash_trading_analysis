import pandas as pd
import numpy as np
from datetime import datetime

# given a series name returns their data, the list of id numbers and the list of unique buyers
def get_opensea_trade_data(series):
    data = pd.read_csv(f"../transaction_files/{series}_transfers.csv")
    ids = data[['id']].copy()
    ids = ids['id'].unique()
    addresses = data[['buyer_address']].copy()
    addresses = addresses['buyer_address'].unique()

    return data, ids, addresses

# given wallet address returns list of ids owned by that wallet and at what times that ownership began
def get_ids_for_address(data, address):
    rows = data.loc[data['buyer_address'] == address]
    ids = rows[['id']].to_numpy()
    times = rows[['time']].to_numpy()
    times = np.array([[datetime.fromisoformat(t)] for t in flatten(times)])
    return ids, times

# given list of wallet addresses returns list of list of ids owned by that wallet and times the ownership began
def get_ids_for_addresses(data, addresses):
    ids_list, times_list = [], []
    for i in addresses:
        ids, times = get_ids_for_address(data, i)
        ids_list.append(ids)
        times_list.append(times)
    return ids_list, times_list

# given an id and the data returns a list of wallets that have held that id and at what times they were
def get_opensea_addresses_times(data, i):
    rows = data.loc[data["id"] == i]
    wallets = rows[['buyer_address']].to_numpy()
    times = rows[['time']].to_numpy()
    try:
        times = np.array([[datetime.fromisoformat(t)] for t in flatten(times)])
    except:
        print(times, i)

    return wallets, times

# given datetimes and a list of wallets and their times return the wallets and times in that
def get_wallets_for_time(wallets, times, range_start, range_end):
    wallets_ret = [w for i, w in enumerate(wallets) if times[i] >= range_start and times[i] <= range_end]
    times_ret = [t for t in times if t >= range_start and t <= range_end]

    return wallets_ret, times_ret

# given data and a list of ids returns the address lists and time lists associated with those ids
def get_all_address_time_pairs(data, ids):
    address_list = []
    times_list = []
    for i in ids:
        wallets, times = get_opensea_addresses_times(data, i)
        address_list.append(wallets)
        times_list.append(times)

    return address_list, times_list

# given lists of lists of wallets and times and start and end datetimes in YYYY-MM-DDTHH:MM:SS format returns those that fit
def get_all_wallets_for_time(wallets_list, times_list, range_start, range_end):
    start, end = datetime.fromisoformat(range_start), datetime.fromisoformat(range_end)

    wallets = []
    times = []
    for i in range(0, len(wallets_list)):
        w = wallets_list[i]
        t = times_list[i]
        wallets.append(get_wallets_for_time(w, t, start, end))
        times.append(get_wallets_for_time(w, t, start, end))

    return wallets, times


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

# given list of addresses checks for loops returns a list of addresses in the loop(s) if a loop is not present returns an empty list
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

# given list of lists of addresses returns list of list of loops
def find_all_loops(addresses_list):
    out = []
    for i in addresses_list:
        loops = find_loops(i)
        out.extend(loops)

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

# given list of sequences of addresses produce list of pairs
def get_list_pairs_for_sequences(sequences):
    pairs = []
    pairs_set = set()
    for i in sequences:
        for j in range(len(i) - 1):
            pair = [i[j], i[j+1]]
            pair_k = (i[j], i[j+1])
            if pair_k not in pairs_set:
                pairs_set.add(pair_k)
                pairs.append(pair)

    return pairs

# given list of associated addresses produce list of pairs
def get_list_pairs_for_associations(sequences):
    pairs = []
    pairs_set = set()
    for i in sequences:
        for j in range(len(i) - 1):
            for k in range(len(i)):
                pair = [i[j], i[k]]
                pair_k = (i[j], i[k])
                if pair_k not in pairs_set and not i[j] == i[k]:
                    pairs_set.add(pair_k)
                    pairs.append(pair)

    return pairs

# creates adjacency matrix given list of pairs returns a labeled pandas dataframe
def create_adjacency_matrix(pairs):
    labels = {k: v for v, k in enumerate(list(set(flatten(pairs))))}
    pairs_rep = [[labels[i] for i in pair] for pair in pairs]
    edges = np.array(pairs_rep)
    matrix = np.zeros((edges.max()+1, edges.max()+1))
    matrix[edges[:,0], edges[:,1]] = 1

    labeled_matrix = pd.DataFrame(matrix, index=labels, columns=labels)

    return labeled_matrix

def remove_out_of_time(data, range_start, range_end):
    start, end = datetime.fromisoformat(range_start), datetime.fromisoformat(range_end)
    times = pd.to_datetime(data['time'])
    mask = (times >= start) & (times <= end)
    rows = data.loc[mask]

    return rows



#data, ids, addresses = get_opensea_trade_data('BAYC')
#common_adds = get_common_addresses(data, 30)
#print(common_adds)
#test = get_node_pairs_from_singles(data, common_adds)
#print(test)
#print(len(test))

#print(remove_out_of_time(data, '2021-04-30T21:11:46', '2021-05-25T17:56:54'))

#print(find_loops([4,3,5,4,6,4,6,3,4]))
#print(get_list_pairs_for_sequences(find_loops([4,3,5,4,6,4,6,3,4])))
#cs = find_common_sequences(data, ids, 7, 7)
#print(cs)
#print(len(cs))

#cs = find_associated_addresses(data, ids, 7, 7)
#print(cs)
#print(len(cs))


#res = create_adjacency_matrix(test)
#print(res)

#ids, times = get_opensea_addresses_times(data, 6)
#print(ids, times)
#t_ids, t_times = get_wallets_for_time(ids, times, datetime(2021, 6, 21, 15, 56, 28), datetime(2021, 12, 22, 19, 23, 15))
#print(t_ids, t_times)

#w, t = get_all_address_time_pairs(data, ids)
#print(get_all_wallets_for_time(w, t, "2021-06-21T15:56:28", "2021-12-22T19:23:15"))

#i, t = get_ids_for_addresses(data, addresses)
#print(i, t)
#print(get_all_wallets_for_time(i, t, "2021-06-21T15:56:28", "2021-12-22T19:23:15"))

#print(get_list_pairs_for_associations([[1,2,3,4,5],[6,7,6,7,6,7]]))

#print(get_list_pairs_for_associations([[1,2,3,4,5],[6,7,6,7,6,7]]))