import pandas as pd

def get_attribute_data(file_name):
    data = pd.read_csv(file_name)
    return data
    

def normalise_attributes(attributes_data):
    attributes_data_num = attributes_data.select_dtypes(include='number')
    attributes_data_norm = (attributes_data_num - attributes_data_num.mean()) / (attributes_data_num.max() - attributes_data_num.min())
    attributes_data_norm = attributes_data_norm.drop(attributes_data_norm.columns[[0]], axis=1)
    attributes_data[attributes_data_norm.columns] = attributes_data_norm
    return attributes_data
