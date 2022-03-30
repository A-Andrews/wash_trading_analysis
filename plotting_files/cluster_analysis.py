import sys
import matplotlib
import matplotlib.pyplot as plt
from os.path import exists
from distance_metrics import normalise_attributes, get_attribute_data
from light_famd import FAMD
from kmodes.kprototypes import KPrototypes

def plot_famd_explained(explained, series, d):
    plt.clf()
    plt.title(f'Proportion of explained variance of factors of {series} for d = {d}')
    plt.ylabel('Proportion of explained variance')
    plt.xlabel('d')
    plt.xticks(range(1,d+1))
    plt.bar(range(1,d+1), explained / explained.sum())
    plt.savefig(f'graphs/famd_explained_{series}_d{d}.png')

def plot_famd_cluster(X_famd, series, d):
    plt.clf()
    plt.title(f'FAMD clustering of {series} for d = {d}')
    plt.scatter(x=X_famd[:,0], y=X_famd[:,1], cmap='tab10')
    plt.savefig(f'graphs/famd_{series}_d{d}.png')

def plot_kprototype_cluster(X_famd, labels, series, k):
    plt.clf()
    plt.title(f'kprototype clustering of {series} for k = {k}')
    plt.scatter(x=X_famd[:,0], y=X_famd[:,1], c=labels, cmap='tab10')
    plt.savefig(f'graphs/kprotocol_{series}_k{k}.png')


def main(argv):
    series = argv[0]
    clustering_type = argv[1]
    n_val = int(argv[2])
    
    data = get_attribute_data(f"attribute_files/{series}_attributes.csv")
    norm_data = normalise_attributes(data)
    norm_data.drop('id', axis=1, inplace=True)
    if clustering_type == "famd":
        famd = FAMD(n_components=n_val)
        famd.fit(norm_data)
        explained_var = famd.explained_variance_
        explained_var_ratio = famd.explained_variance_ratio_
        norm_data_famd = famd.transform(norm_data)
        if not exists(f'graphs/famd_explained_{series}_d{n_val}.png'): plot_famd_explained(explained_var, series, n_val)
        if not exists(f'graphs/famd_{series}_d{n_val}.png'): plot_famd_cluster(norm_data_famd, series, n_val)
    if clustering_type == "kprotocol":
        categorical_col = norm_data.select_dtypes(include='object').columns.tolist()
        categorical_col_ind = norm_data.columns.get_indexer(categorical_col).tolist()
        clusters = KPrototypes(n_clusters = n_val).fit_predict(norm_data, categorical=categorical_col_ind)
        famd = FAMD(n_components=2)
        famd.fit(norm_data)
        norm_data_famd = famd.transform(norm_data)
        if not exists(f'graphs/kprotocol_{series}_k{n_val}.png'): plot_kprototype_cluster(norm_data_famd, clusters, series, n_val)
        

if __name__ == "__main__":
   main(sys.argv[1:])