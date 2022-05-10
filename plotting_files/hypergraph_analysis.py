import sys
import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx
import numpy as np
from extracting_trade_list import *

def plot_hypergraph(ownership):
    hnx.drawing.rubber_band.draw(ownership)
    plt.show()

def basic_hypergraph_addresses(data, common_number, amount, series):
    common_addresses = get_common_addresses(data, common_number)
    top_addresses = get_topx_common(common_addresses, amount)
    
    ownership = get_addresses_ids_dict(data, top_addresses.index.to_numpy())
    h = hnx.Hypergraph(ownership)
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


if __name__ == "__main__":
   main(sys.argv[1:])