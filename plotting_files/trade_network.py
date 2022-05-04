import sys
from extracting_trade_list import *
import networkx as nx
import matplotlib.pyplot as plt

def list_for_time_period():
    return 0

def create_graph_for_one(addresses, i, time):

    return 0



def create_adjacency_graph(adj_mat):
    nx.draw_networkx(nx.from_pandas_adjacency(adj_mat), node_size = 30, font_size=1)

def common_singles_network(data, common_number, series):
    common_addresses = get_common_addresses(data, common_number)
    pairs = get_node_pairs_from_singles(data, common_addresses)
    adj_mat = create_adjacency_matrix(pairs)
    create_adjacency_graph(adj_mat)
    plt.show()

def common_pairs_network(data, common_number, series):
    pairs = get_common_pairs(data, common_number)
    pairs = get_node_pairs_from_pairs(pairs)
    adj_mat = create_adjacency_matrix(pairs)
    create_adjacency_graph(adj_mat)
    plt.show()

def common_sequences_network(data, ids, series, min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_associations(sequences)
    adj_mat = create_adjacency_matrix(pairs)
    create_adjacency_graph(adj_mat)
    plt.show()

def main(argv):
    series = argv[0]
    network_type = argv[1]
    time_range_start = argv[2]
    time_range_end = argv[3]
    common_number = int(argv[4])

    data = None
    ids = None

    if series == 'BAYC' or series == 'cryptopunk':
        data, ids, addresses = get_opensea_trade_data(series)
    if network_type == 'common_singles':
        common_singles_network(data, common_number, series)
    if network_type == 'common_pairs':
        common_pairs_network(data, common_number, series)
    if network_type == 'common_sequences':
        common_sequences_network(data, ids, series, common_number, common_number)
        


if __name__ == "__main__":
   main(sys.argv[1:])