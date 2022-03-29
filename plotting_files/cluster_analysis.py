from distance_metrics import normalise_attributes, get_attribute_data

print(normalise_attributes(get_attribute_data("attribute_files/axie_attributes.csv")).dtypes)