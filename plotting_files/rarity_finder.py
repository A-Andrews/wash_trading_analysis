import pandas as pd

# Replaces values with the frequency of their occurance in that column
def replace_rarity(data):
    for column in data:
        data[column] = data[column].map(data[column].value_counts()/data.shape[0])

    data = data[[i for i in data if len(set(data[i]))>1]]
    return data

