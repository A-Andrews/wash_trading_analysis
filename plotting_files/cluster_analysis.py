import sys
import matplotlib.pyplot as plt
from os.path import exists
from distance_metrics import normalise_attributes, get_attribute_data
from rarity_finder import replace_rarity
from light_famd import FAMD
from kmodes.kprototypes import KPrototypes
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def plot_famd_explained(explained, series, d, rarity = False):
    plt.clf()

    if rarity:
        title = f'Proportion of explained variance of factors of {series} for d = {d} (PCA)'
        save_path = f'../graphs/pca_explained_{series}_d{d}_rarity.png'
    
    else:
        title = f'Proportion of explained variance of factors of {series} for d = {d}'
        save_path = f'../graphs/famd_explained_{series}_d{d}.png'

    plt.title(title)
    plt.ylabel('Proportion of explained variance')
    plt.xlabel('d')
    plt.xticks(range(1,d+1))
    plt.bar(range(1,d+1), explained / explained.sum())
    plt.savefig(save_path)

def plot_famd_cluster(X_famd, series, d, rarity = False):
    plt.clf()
    
    if rarity:
        title = f'PCA clustering of {series} for d = {d}'
        save_path = f'../graphs/pca_{series}_d{d}_rarity.png'
    
    else:
        title = f'FAMD clustering of {series} for d = {d}'
        save_path = f'../graphs/pca_{series}_d{d}.png'

    plt.title(title)
    plt.scatter(x=X_famd[:,0], y=X_famd[:,1], cmap='tab10')
    plt.savefig(save_path)

def plot_kprototype_cluster(X_famd, labels, series, k, rarity = False):
    plt.clf()

    if rarity:
        title = f'kmeans clustering of {series} for k = {k} (Rarity)'
        save_path = f'../graphs/kmeans_{series}_k{k}_rarity.png'
    
    else:
        title = f'kprototype clustering of {series} for k = {k}'
        save_path = f'../graphs/kprototype_{series}_k{k}.png'

    plt.title(title)
    plt.scatter(x=X_famd[:,0], y=X_famd[:,1], c=labels, cmap='tab10')
    plt.savefig(save_path)


def main(argv):
    series = argv[0]
    clustering_type = argv[1]
    n_val = int(argv[2])
    
    data = get_attribute_data(f"../attribute_files/{series}_attributes.csv")
    norm_data = normalise_attributes(data)
    norm_data.drop('id', axis=1, inplace=True)

    if clustering_type == "famd":
        famd = FAMD(n_components=n_val)
        print(norm_data)
        famd.fit(norm_data)
        explained_var = famd.explained_variance_
        norm_data_famd = famd.transform(norm_data)
        if not exists(f'../graphs/famd_explained_{series}_d{n_val}.png'): plot_famd_explained(explained_var, series, n_val)
        if not exists(f'../graphs/famd_{series}_d{n_val}.png'): plot_famd_cluster(norm_data_famd, series, n_val)

    if clustering_type == "pca-rarity":
        rarity_data = replace_rarity(data)
        norm_rarity_data = normalise_attributes(rarity_data)
        pca = PCA(n_components=n_val)
        norm_data_pca = pca.fit_transform(norm_rarity_data)
        explained_var = pca.explained_variance_ratio_
        if not exists(f'../graphs/pca_explained_{series}_d{n_val}_rarity.png'): plot_famd_explained(explained_var, series, n_val, rarity = True)
        if not exists(f'../graphs/pca_{series}_d{n_val}_rarity.png'): plot_famd_cluster(norm_data_pca, series, n_val, rarity = True)

    if clustering_type == "kprototype":
        categorical_col = norm_data.select_dtypes(include='object').columns.tolist()
        categorical_col_ind = norm_data.columns.get_indexer(categorical_col).tolist()
        clusters = KPrototypes(n_clusters = n_val).fit_predict(norm_data, categorical=categorical_col_ind)
        famd = FAMD(n_components=2)
        famd.fit(norm_data)
        norm_data_famd = famd.transform(norm_data)
        if not exists(f'../graphs/kprototype_{series}_k{n_val}.png'): plot_kprototype_cluster(norm_data_famd, clusters, series, n_val)

    if clustering_type == "kmeans-rarity":
        rarity_data = replace_rarity(data)
        norm_rarity_data = normalise_attributes(rarity_data)
        clusters = KMeans(n_clusters = n_val).fit_predict(norm_rarity_data)
        pca = PCA(n_components=n_val)
        norm_data_pca = pca.fit_transform(norm_rarity_data)
        if not exists(f'../graphs/kmeans_{series}_k{n_val}_rarity.png'): plot_kprototype_cluster(norm_data_pca, clusters, series, n_val, rarity = True)
        

if __name__ == "__main__":
   main(sys.argv[1:])