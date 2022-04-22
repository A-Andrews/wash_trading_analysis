import sys
import extracting_trade_list
from plotting_files.extracting_trade_list import get_opensea_trade_data
import networkx as nx

def list_for_time_period():
    return 0

def create_graph_for_one(addresses, i, time):

    return 0

def main(argv):
    series = argv[0]
    network_type = argv[1]
    time_range_start = argv[2]
    time_range_end = argv[3]

    if series == 'BAYC':
        data, ids, addresses = get_opensea_trade_data(series)

if __name__ == "__main__":
   main(sys.argv[1:])