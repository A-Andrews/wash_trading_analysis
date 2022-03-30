import sys
import matplotlib
import matplotlib.pyplot as plt
from distance_metrics import normalise_attributes, get_attribute_data
from light_famd import FAMD

def plot_pca_explained(explained, series):
    plt.title(f'Proportion of explained variance of principal components of {series} for d = {len(explained)}')
    plt.ylabel('Proportion of explained variance')
    plt.xlabel('d')
    plt.xticks(range(1,len(explained)+1))
    plt.bar(range(1,len(explained)+1), explained / explained.sum())
    plt.savefig(f'graphs/pca_explained_{series}_d{len(explained)}.png')


def main(argv):
    series = argv[0]
    clustering_type = argv[1]
    data = get_attribute_data(f"attribute_files/{series}_attributes.csv")
    norm_data = normalise_attributes(data)
    norm_data.drop('id', 1, inplace=True)
    if clustering_type == "famd":
        famd = FAMD(n_components=2)
        famd.fit(norm_data)
        explained_var = famd.explained_variance_
        explained_var_ratio = famd.explained_variance_ratio_
        norm_data_famd = famd.transform(norm_data)
        plot_pca_explained(explained_var, series)

if __name__ == "__main__":
   main(sys.argv[1:])