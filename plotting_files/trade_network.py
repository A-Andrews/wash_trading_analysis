import sys
from extracting_trade_list import *
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta

data = None
ids = None
names = None
addresses = None

common_number = None
series = None

nodes = None
edges = None
labels = None

ani = None

earliest_date = '2021-04-30T00:00:00'

def list_for_time_period():
    return 0

def create_graph_for_one(addresses, i, time):
    return 0



def create_adjacency_graph(adj_mat, weights):
    g = nx.from_pandas_adjacency(adj_mat)
    list_degree=list(g.degree())
    pos = nx.spring_layout(g, seed=4)
    nodes_list, degree = map(list, zip(*list_degree))
    nodes_amounts = get_owned_nums(data, replace_mixed_names_addresses(data, nodes_list))
    node_size = [(v * 0.3) for v in nodes_amounts]

    nodes = nx.draw_networkx_nodes(g, pos = pos, nodelist=nodes_list, node_size = node_size, alpha = 0.6)
    labels = nx.draw_networkx_labels(g, pos, font_size = 6, alpha = 0.7)

    weights_rgb = [plt.cm.plasma(i / max(weights)) for i in weights]
    cmap = plt.cm.plasma
    edges = nx.draw_networkx_edges(g, pos, edge_color = weights_rgb, edge_cmap = cmap, nodelist = nodes_list, node_size = node_size, width = 2, arrowsize=4, arrows = True)

    pc = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin = min(weights), vmax=max(weights)))
    plt.colorbar(pc)

    return nodes, edges, labels, g

def common_singles_network(common_number):
    common_addresses = get_common_addresses(data, common_number)
    pairs = get_node_pairs_from_singles(data, common_addresses)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(adj_mat, weights_p)

def common_pairs_network(common_number):
    pairs = get_common_pairs(data, common_number)
    pairs = get_node_pairs_from_pairs(pairs)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(adj_mat, weights_p)

def common_sequences_network(min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_sequences(sequences)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(adj_mat, weights_p)

def common_associations_network(min_length = 1, min_occurances = 1):
    sequences = find_associated_addresses(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_associations(sequences)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(adj_mat, weights_p)

def simple_loops_network(min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    loops = find_all_loops(sequences)
    pairs = get_list_pairs_for_sequences(loops)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(adj_mat, weights_p)

def update(days, g):
    global data
    end_date = datetime.fromisoformat(earliest_date) + timedelta(days=days)
    data = remove_out_of_time(data, earliest_date, end_date.isoformat())
    edges = nx.draw_networkx_edges(g, width = days, arrowsize=4, arrows = True)

def animated_singles(common_number, interval):
    global ani
    common_addresses = get_common_addresses(data, common_number)
    pairs = get_node_pairs_from_singles(data, common_addresses)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    nodes, edges, labels, g = create_adjacency_graph(adj_mat, weights_p)
    fig = plt.figure(figsize=(8,8))

    ani = FuncAnimation(fig, update, fargs=(g), frames=100, interval=1000, repeat=True)



def main(argv):
    global series, common_number
    series = argv[0]
    network_type = argv[1]
    time_range_start = argv[2]
    time_range_end = argv[3]
    common_number = int(argv[4])

    if series == 'BAYC' or series == 'cryptopunk':
        global data, ids, addresses
        data, ids, addresses = get_opensea_trade_data(series)
        if time_range_start != '0':
            data = remove_out_of_time(data, time_range_start, time_range_end)
    if network_type == 'common_singles':
        common_singles_network(common_number)
    if network_type == 'common_pairs':
        common_pairs_network(common_number)
    if network_type == 'common_sequences':
        common_sequences_network(common_number, common_number)
    if network_type == 'common_associations':
        common_associations_network(common_number, common_number)
    if network_type == 'simple_loops':
        simple_loops_network(common_number, common_number)
    if network_type == 'animated_singles':
        animated_singles(common_number, 10)

    plt.show()
        


if __name__ == "__main__":
   main(sys.argv[1:])