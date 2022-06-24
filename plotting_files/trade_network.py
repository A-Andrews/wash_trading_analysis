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

# plots network graph
def create_adjacency_graph(adj_mat, weights):
    g = nx.MultiDiGraph()
    g.add_edges_from(adj_mat)

    list_degree=list(g.degree())
    pos = nx.spring_layout(g, k = 0.18, seed=10)
    nodes_list, degree = map(list, zip(*list_degree))
    nodes_amounts = get_owned_nums(data, replace_mixed_names_addresses(data, nodes_list))
    node_size = [(v * 0.3) for v in nodes_amounts]

    nodes = nx.draw_networkx_nodes(g, pos = pos, nodelist=nodes_list, node_size = node_size, alpha = 0.6)
    labels = nx.draw_networkx_labels(g, pos, font_size = 5, alpha = 0.7)

    weights_rgb = [plt.cm.plasma(i / max(weights)) for i in weights]
    cmap = plt.cm.plasma
    edges = nx.draw_networkx_edges(g, pos, edge_color = weights_rgb, edge_cmap = cmap, nodelist = nodes_list, node_size = node_size, width = 2, arrowsize=4, arrows = True, connectionstyle='arc3,rad=0.2')

    pc = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin = min(weights), vmax=max(weights)))
    plt.colorbar(pc)

    return nodes, edges, labels, g

# plots network graph of single addresses occurring over a threshold
def common_singles_network(common_number):
    common_addresses = get_common_addresses(data, common_number)
    pairs = get_node_pairs_from_singles(data, common_addresses)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(pairs, weights_p)

# plots network graph of pairs of addresses occurring over a threshold
def common_pairs_network(common_number):
    pairs = get_common_pairs(data, common_number)
    pairs = get_node_pairs_from_pairs(pairs)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(pairs, weights_p)

# returns a latex formated table of pairs of addresses occurring over a threshold
def common_pairs_network_text(common_number):
    pairs = get_common_pairs(data, common_number)
    pairs = get_node_pairs_from_pairs(pairs)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)

    with open(f'../graphs/{series}_pairs_network_{common_number}.txt', 'w') as f:
        f.write('\\begin{table}[H]\n\centering\n\\begin{tabular}{ |c|c||c|  }\n\hline\n\multicolumn{3}{|c|}{BAYC Feature List} \\\ \n\hline\nSender & Reciever & Trades\\\ \n\hline\n')
        for n, i in enumerate(pairs):
            seller = i[0]
            buyer = i[1]
            trades = weights_p[n]
            f.write(f'{seller} & {buyer} & {trades} \\\ \n\hline\n')
        f.write('\end{tabular}\n\label{}\n\caption{}\n\end{table}')

# returns the addresses as a latex table for pairs occurring over a threshold
def common_pairs_network_text_addresses(common_number):
    pairs = get_common_pairs(data, common_number)
    pairs = get_node_pairs_from_pairs(pairs)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)

    amounts = dict.fromkeys(flatten(pairs), 0)

    total = 0

    for n, i in enumerate(pairs):
        seller = i[0]
        buyer = i[1]
        trades = weights_p[n]

        amounts[seller] += trades
        amounts[buyer] += trades
        total += trades

    with open(f'../graphs/{series}_pairs_network_addresses_{common_number}.txt', 'w') as f:
        f.write('\\begin{table}[H]\n\centering\n\\begin{tabular}{ c c c }\n\hline\n \\\ \n\hline\n Address & Trade Involvement & Wash Trading Likelihood\\\ \n\hline\n')
        for k, v in amounts.items():
            f.write(f'{k} & {v} & 0 \\\ \n')
        f.write('\hline \\\ \n \end{tabular}\n\label{}\n\caption{'+ str(total) +'}\n\end{table}')

# plots network graph of sequences of a certain length that occur a certain number of times
def common_sequences_network(min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_sequences(sequences)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(pairs, weights_p)

# plots association graphs of addresses that occur together in groups of a specified size a certain number of times
def common_associations_network(min_length = 1, min_occurances = 1):
    sequences = find_associated_addresses(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_associations(sequences)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(pairs, weights_p)

# plots loops of a certain size that occur a certain number of times
def simple_loops_network(min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, 10)
    loops = find_all_loops(sequences)
    pairs = get_list_pairs_for_sequences(loops)
    weights_p = get_trades_between_pairs(data, pairs)
    print(weights_p)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_adjacency_matrix(pairs)
    return create_adjacency_graph(pairs, weights_p)

def simple_loops_text(min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, 10)
    loops = find_all_loops(sequences)
    pairs = get_list_pairs_for_sequences(loops)
    print(pairs)
    weights_p = get_trades_between_pairs(data, pairs)
    print(weights_p)
    pairs = replace_pairs_names(data, pairs)

    with open(f'../graphs/{series}_loops_network_{common_number}.txt', 'w') as f:
        f.write('\\begin{table}[H]\n\centering\n\\begin{tabular}{ |c|c||c|  }\n\hline\n\multicolumn{3}{|c|}{} \\\ \n\hline\nSender & Reciever & Trades\\\ \n\hline\n')
        for n, i in enumerate(pairs):
            seller = i[0]
            buyer = i[1]
            trades = weights_p[n]
            f.write(f'{seller} & {buyer} & {trades} \\\ \n\hline\n')
        f.write('\end{tabular}\n\label{}\n\caption{}\n\end{table}')

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
    nodes, edges, labels, g = create_adjacency_graph(pairs, weights_p)
    fig = plt.figure(figsize=(8,8))

    ani = FuncAnimation(fig, update, fargs=(g), frames=100, interval=1000, repeat=True)

def main(argv):
    global series, common_number
    series = argv[0]
    network_type = argv[1]
    time_range_start = argv[2]
    time_range_end = argv[3]
    common_number = int(argv[4])

    plt.figure(figsize=(20,8))

    if series == 'BAYC' or series == 'cryptopunk':
        global data, ids, addresses
        data, ids, addresses = get_opensea_trade_data(series, True)
        if time_range_start != '0':
            data = remove_out_of_time(data, time_range_start, time_range_end)
    if network_type == 'common_singles':
        common_singles_network(common_number)
    if network_type == 'common_pairs':
        common_pairs_network(common_number)
    if network_type == 'common_pairs_text':
        common_pairs_network_text(common_number)
    if network_type == 'common_pairs_text_add':
        common_pairs_network_text_addresses(common_number)
    if network_type == 'common_sequences':
        common_sequences_network(common_number, common_number)
    if network_type == 'common_associations':
        common_associations_network(common_number, common_number)
    if network_type == 'simple_loops':
        simple_loops_network(common_number, common_number)
    if network_type == 'animated_singles':
        animated_singles(common_number, 10)
    if network_type == 'simple_loops_text':
        simple_loops_text(common_number, common_number)
    
    plt.show()      

if __name__ == "__main__":
   main(sys.argv[1:])