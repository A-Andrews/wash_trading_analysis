import sys
import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx
import numpy as np
from extracting_trade_list import *

def plot_hypergraph(ownership):
    hnx.drawing.rubber_band.draw(ownership, node_radius = 1)
    plt.show()

def basic_hypergraph_addresses(data, common_number, amount, series, display_ids = False, id_occurances = 0):
    common_addresses = get_common_addresses(data, common_number)
    top_addresses = get_topx_common(common_addresses, amount)
    
    ownership = get_addresses_ids_dict(data, top_addresses.index.to_numpy())

    if id_occurances == 0:
        ownership = get_addresses_ids_dict(data, top_addresses.index.to_numpy())
    else:
        ownership = get_all_pairs_ownership_dict(data, top_addresses.index.to_numpy(), id_occurances)

    h = hnx.Hypergraph(ownership)

    if display_ids: h = h.dual()
    plot_hypergraph(h)

def basic_hypergraph_pairs(data, common_number, amount, series, display_ids = False, id_occurances = 0):
    common_pairs = get_common_pairs(data, common_number)
    top_pairs = get_topx_common(common_pairs, amount)
    top_pairs = get_node_pairs_from_pairs(top_pairs)

    addresses = flatten(top_pairs)

    if id_occurances == 0:
        ownership = get_addresses_ids_dict(data, addresses)
    else:
        ownership = get_all_pairs_ownership_dict(data, addresses, id_occurances)

    h = hnx.Hypergraph(ownership)

    if display_ids: h = h.dual()
    plot_hypergraph(h)

def basic_hypergraph_sequences(data, ids, series, min_length = 1, min_occurances = 1, display_ids = False, id_occurances = 0):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_sequences(sequences)

    addresses = flatten(pairs)
    if id_occurances == 0:
        ownership = get_addresses_ids_dict(data, addresses)
    else:
        ownership = get_all_pairs_ownership_dict(data, addresses, id_occurances)

    h = hnx.Hypergraph(ownership)

    if display_ids: h = h.dual()
    plot_hypergraph(h)

def basic_hypergraph_associations(data, ids, series, min_length = 1, min_occurances = 1, display_ids = False, id_occurances = 0):
    sequences = find_associated_addresses(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_associations(sequences)

    addresses = flatten(pairs)

    if id_occurances == 0:
        ownership = get_addresses_ids_dict(data, addresses)
    else:
        ownership = get_all_pairs_ownership_dict(data, addresses, id_occurances)

    h = hnx.Hypergraph(ownership)

    if display_ids: h = h.dual()
    plot_hypergraph(h)

def basic_hypergraph_loops(data, ids, series, min_length = 1, min_occurances = 1, display_ids = False, id_occurances = 0):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    loops = find_all_loops(sequences)
    pairs = get_list_pairs_for_sequences(loops)

    addresses = flatten(pairs)

    if id_occurances == 0:
        ownership = get_addresses_ids_dict(data, addresses)
    else:
        ownership = get_all_pairs_ownership_dict(data, addresses, id_occurances)
    h = hnx.Hypergraph(ownership)

    if display_ids: h = h.dual()
    plot_hypergraph(h)


def main(argv):
    series = argv[0]
    network_type = argv[1]
    time_range_start = argv[2]
    time_range_end = argv[3]
    common_number = int(argv[4])
    amount = int(argv[5])

    data = None
    ids = None

    if series == 'BAYC' or series == 'cryptopunk':
        data, ids, addresses = get_opensea_trade_data(series)
        if time_range_start != '0':
            data = remove_out_of_time(data, time_range_start, time_range_end)
    if network_type == 'basic_hypergraph_addresses':
        basic_hypergraph_addresses(data, common_number, amount, series)
    elif network_type == 'basic_hypergraph_ids':
        basic_hypergraph_addresses(data, common_number, amount, series, display_ids = True)
    elif network_type == 'basic_hypergraph_pairs':
        basic_hypergraph_pairs(data, common_number, amount, series)
    elif network_type == 'basic_hypergraph_pairs_ids':
        basic_hypergraph_pairs(data, common_number, amount, series, display_ids = True)
    elif network_type == 'basic_hypergraph_sequences':
        basic_hypergraph_sequences(data, ids, series, common_number, amount)
    elif network_type == 'basic_hypergraph_sequences_ids':
        basic_hypergraph_sequences(data, ids, series, common_number, amount, display_ids = True)
    elif network_type == 'basic_hypergraph_associations':
        basic_hypergraph_associations(data, ids, series, common_number, amount)
    elif network_type == 'basic_hypergraph_associations_ids':
        basic_hypergraph_associations(data, ids, series, common_number, amount, display_ids = True)
    elif network_type == 'basic_hypergraph_loops':
        basic_hypergraph_loops(data, ids, series, common_number, amount)
    elif network_type == 'basic_hypergraph_loops_ids':
        basic_hypergraph_loops(data, ids, series, common_number, amount, display_ids = True)
    elif network_type == 'restricted_hypergraph_addresses':
        basic_hypergraph_addresses(data, common_number, amount, series, id_occurances = common_number)
    elif network_type == 'restricted_hypergraph_pairs':
        basic_hypergraph_pairs(data, common_number, amount, series, id_occurances = common_number)
    elif network_type == 'restricted_hypergraph_sequences':
        basic_hypergraph_sequences(data, ids, series, common_number, amount, id_occurances = common_number)
    elif network_type == 'restricted_hypergraph_associations':
        basic_hypergraph_associations(data, ids, series, common_number, amount, id_occurances = common_number)
    elif network_type == 'restricted_hypergraph_loops':
        basic_hypergraph_loops(data, ids, series, common_number, amount, id_occurances = common_number)



if __name__ == "__main__":
   main(sys.argv[1:])