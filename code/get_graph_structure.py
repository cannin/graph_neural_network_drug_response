import sys
import warnings
from os import listdir
from os.path import exists

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from joblib import Parallel, delayed

warnings.filterwarnings("ignore")

from sklearn.decomposition import PCA
from tqdm import tqdm


def get_pca(hidden, hidden_data_path, sample_index):
    pca = pd.DataFrame()

    print("Start to calculate the PCA of each hidden layer.")
    for i in tqdm(hidden):
        X = pd.read_csv(
            hidden_data_path + i,
            sep=" ",
            header=None,
        ).loc[sample_index]

        X_pca = PCA(n_components=1).fit_transform(X)
        pca = pd.concat([pca, pd.DataFrame(X_pca).T])

    pca.columns = sample_index
    pca.index = [i.split(".")[0] for i in hidden]

    return pca


def get_single_hidden_layer(hidden, hidden_data_path, sample_index):
    df = pd.DataFrame()

    print("Get each hidden layer.")
    for i in tqdm(hidden):
        X = pd.read_csv(
            hidden_data_path + i,
            sep=" ",
            header=None,
        ).loc[sample_index]

        df = pd.concat([df, X.T])

    df.columns = sample_index
    df.index = [i.split(".")[0] for i in hidden]

    return df


def get_weight_parallel(gene, G, pca):
    paths = list(nx.all_simple_paths(G, source="GO:0008150", target=gene))

    if len(paths) != 1:
        path = set()
        for i in paths:
            path = path | set(i)
    else:
        path = paths[0]

    path.remove(gene)
    return [gene] + list(np.sum(pca.loc[path], axis=0))


def get_weight(sample_index, hidden_data_path, go):
    sample_index = sample_index.split(",")
    sample_index = list(map(int, sample_index))
    hidden = listdir(hidden_data_path)
    hidden = [i for i in hidden if "GO" in i]

    X = pd.read_csv(
        "/export/scratch/inoue019/Hidden_135/GO:0000038.hidden",
        sep=" ",
        header=None,
    )

    if X.shape[1] == 1:
        GO_terms = get_single_hidden_layer(hidden, hidden_data_path, sample_index)
    else:
        GO_terms = get_pca(hidden, hidden_data_path, sample_index)

    nodes = list(set(go[0]) | set(go[1]))
    genes = set(go[["GO" not in i for i in go[1]]][1])
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(list(go.itertuples(index=False, name=None)))

    print("Start to calculate the weight of each gene.")
    t = Parallel(n_jobs=-1)(
        delayed(get_weight_parallel)(gene, G, GO_terms) for gene in tqdm(list(genes))
    )
    t = pd.DataFrame(t)
    t.index = list(t[0])
    t = t.drop(0, axis=1)
    t.columns = sample_index

    weight = pd.concat([GO_terms, t])
    weight.to_csv("weight.csv")


def get_graph_info(sample_index, hidden_data_path, onto_file):
    go = pd.read_table(onto_file, header=None)[[0, 1]]
    go.to_csv(
        "./graph.csv",
    )

    get_weight(sample_index, hidden_data_path, go)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 4:
        if exists(args[2]) and exists(args[3]):
            get_graph_info(args[1], args[2], args[3])
        else:
            print("Error: File not found")
    else:
        print("Looks the number of arguments is wrong.")
        print(
            "Usage: python get_graph_structure.py sample_index hidden_data_path ontology"
        )
        sys.exit(1)
