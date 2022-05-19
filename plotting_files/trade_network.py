import sys
from extracting_trade_list import *
import networkx as nx
import matplotlib.pyplot as plt

def list_for_time_period():
    return 0

def create_graph_for_one(addresses, i, time):

    return 0



def create_adjacency_graph(data, adj_mat, weights):
    g = nx.from_pandas_adjacency(adj_mat)
    list_degree=list(g.degree())
    pos = nx.spring_layout(g, seed=4)
    nodes, degree = map(list, zip(*list_degree))
    nodes_amounts = get_owned_nums(data, replace_mixed_names_addresses(data, nodes))
    nx.draw_networkx(g, pos = pos, font_size=6, nodelist=nodes, node_size=[(v * 0.7)+1 for v in nodes_amounts], arrowstyle='-|>')

    for i, e in enumerate(g.edges):
        nx.draw_networkx_edges(g, pos, edgelist=[e], width = weights[i]*0.1)

def common_singles_network(data, common_number, series):
    common_addresses = get_common_addresses(data, common_number)
    pairs = get_node_pairs_from_singles(data, common_addresses)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    create_adjacency_graph(data, adj_mat, weights_p)
    plt.show()

def common_pairs_network(data, common_number, series):
    pairs = get_common_pairs(data, common_number)
    pairs = get_node_pairs_from_pairs(pairs)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    create_adjacency_graph(data, adj_mat, weights_p)
    plt.show()

def common_sequences_network(data, ids, series, min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_sequences(sequences)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    create_adjacency_graph(data, adj_mat, weights_p)
    plt.show()

def common_associations_network(data, ids, series, min_length = 1, min_occurances = 1):
    sequences = find_associated_addresses(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_associations(sequences)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    create_adjacency_graph(data, adj_mat, weights_p)
    plt.show()

def simple_loops_network(data, ids, series, min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    loops = find_all_loops(sequences)
    pairs = get_list_pairs_for_sequences(loops)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    create_adjacency_graph(data, adj_mat, weights_p)
    plt.show()


def main(argv):
    series = argv[0]
    network_type = argv[1]
    time_range_start = argv[2]
    time_range_end = argv[3]
    common_number = int(argv[4])

    data = None
    ids = None
    names = None

    if series == 'BAYC' or series == 'cryptopunk':
        data, ids, addresses = get_opensea_trade_data(series)
        if time_range_start != '0':
            data = remove_out_of_time(data, time_range_start, time_range_end)
    if network_type == 'common_singles':
        common_singles_network(data, common_number, series)
    if network_type == 'common_pairs':
        common_pairs_network(data, common_number, series)
    if network_type == 'common_sequences':
        common_sequences_network(data, ids, series, common_number, common_number)
    if network_type == 'common_associations':
        common_associations_network(data, ids, series, common_number, common_number)
    if network_type == 'simple_loops':
        simple_loops_network(data, ids, series, common_number, common_number)
        


if __name__ == "__main__":
   main(sys.argv[1:])