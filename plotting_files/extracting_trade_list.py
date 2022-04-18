import pandas as pd

def get_opensea_trade_data(series):
    data = pd.read_csv(f"transaction_files/{series}_transfers.csv")
    ids = data[['id']].copy()
    ids = ids['id'].unique()

    # Get lists of rows associated with particular time stamp
    for i in ids:
        return 0

get_opensea_trade_data('BAYC')
