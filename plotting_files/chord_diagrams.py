import sys
from extracting_trade_list import *
import networkx as nx
import matplotlib.pyplot as plt
from chord import Chord
from mpl_chord_diagram import chord_diagram

def plot_chord(matrix):
    chord_diagram(matrix.to_numpy(), list(matrix.columns.values), fontsize = 4, rotate_names = True, chordwidth = 0.1, pad = 4)
    #Chord(matrix.values.tolist(), list(matrix.columns.values)).to_html()

def simple_common_chord(data, common_number, amount, series):
    common_addresses = get_common_addresses(data, common_number)
    pairs = get_node_pairs_from_singles(data, common_addresses)
    top_pairs = get_topx_common_list(pairs, amount)
    weights_p = get_trades_between_pairs(data, top_pairs)
    top_pairs = replace_pairs_names(data, top_pairs)
    adj_mat = create_weighted_adjacency_matrix(top_pairs, weights_p)
    plot_chord(adj_mat)

def simple_common_pairs_chord(data, common_number, amount, series):
    pairs = get_common_pairs(data, common_number)
    top_pairs = get_topx_common(pairs, amount)
    top_pairs = get_node_pairs_from_pairs(top_pairs)
    weights_p = get_trades_between_pairs(data, top_pairs)
    top_pairs = replace_pairs_names(data, top_pairs)
    adj_mat = create_weighted_adjacency_matrix(top_pairs, weights_p)
    plot_chord(adj_mat)

def simple_common_sequences_chord(data, ids, series, min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_sequences(sequences)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_weighted_adjacency_matrix(pairs, weights_p)
    plot_chord(adj_mat)

def simple_common_associations_chord(data, ids, series, min_length = 1, min_occurances = 1):
    sequences = find_associated_addresses(data, ids, min_length, min_occurances)
    pairs = get_list_pairs_for_associations(sequences)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_weighted_adjacency_matrix(pairs, weights_p)
    plot_chord(adj_mat)

def simple_common_loops_chord(data, ids, series, min_length = 1, min_occurances = 1):
    sequences = find_common_sequences(data, ids, min_length, min_occurances)
    loops = find_all_loops(sequences)
    pairs = get_list_pairs_for_sequences(loops)
    weights_p = get_trades_between_pairs(data, pairs)
    pairs = replace_pairs_names(data, pairs)
    adj_mat = create_weighted_adjacency_matrix(pairs, weights_p)
    plot_chord(adj_mat)

def main(argv):
    series = argv[0]
    network_type = argv[1]
    time_range_start = argv[2]
    time_range_end = argv[3]
    common_number = int(argv[4])
    amount = int(argv[5])

    data = None
    ids = None

    plt.figure(figsize=(20,8))

    if series == 'BAYC' or series == 'cryptopunk':
        data, ids, addresses = get_opensea_trade_data(series)
        if time_range_start != '0':
            data = remove_out_of_time(data, time_range_start, time_range_end)
    if network_type == 'simple_common_chord':
        simple_common_chord(data, common_number, amount, series)
    elif network_type == 'simple_common_pairs_chord':
        simple_common_pairs_chord(data, common_number, amount, series)
    elif network_type == 'simple_common_sequences_chord':
        simple_common_sequences_chord(data, ids, series, min_length=common_number, min_occurances=amount)
    elif network_type == 'simple_common_associations_chord':
        simple_common_associations_chord(data, ids, series, common_number, amount)
    elif network_type == 'simple_common_loops_chord':
        simple_common_loops_chord(data, ids, series, common_number, amount)

    plt.show()
        

if __name__ == "__main__":
   main(sys.argv[1:])