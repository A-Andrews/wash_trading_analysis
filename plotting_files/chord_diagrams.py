import sys
from extracting_trade_list import *
import networkx as nx
import matplotlib.pyplot as plt
from chord import Chord
from mpl_chord_diagram import chord_diagram

def plot_chord(matrix):
    chord_diagram(matrix.to_numpy(), list(matrix.columns.values), fontsize = 4, rotate_names = True, chordwidth = 0.1, pad = 4)
    plt.show()
    #Chord(matrix.values.tolist(), list(matrix.columns.values)).to_html()

def simple_common_chord(data, common_number, amount, series):
    common_addresses = get_common_addresses(data, common_number)
    pairs = get_node_pairs_from_singles(data, common_addresses)
    top_pairs = get_topx_common_list(pairs, amount)
    adj_mat = create_adjacency_matrix(top_pairs)
    plot_chord(adj_mat)

def simple_common_pairs_chord(data, common_number, amount, series):
    pairs = get_common_pairs(data, common_number)
    top_pairs = get_topx_common(pairs, amount)
    top_pairs = get_node_pairs_from_pairs(top_pairs)
    adj_mat = create_adjacency_matrix(top_pairs)
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

    if series == 'BAYC' or series == 'cryptopunk':
        data, ids, addresses = get_opensea_trade_data(series)
        if time_range_start != '0':
            data = remove_out_of_time(data, time_range_start, time_range_end)
    if network_type == 'simple_common_chord':
        simple_common_chord(data, common_number, amount, series)
    elif network_type == 'simple_common_pairs_chord':
        simple_common_pairs_chord(data, common_number, amount, series)
        

if __name__ == "__main__":
   main(sys.argv[1:])