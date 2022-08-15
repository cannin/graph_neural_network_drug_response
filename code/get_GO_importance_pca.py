import sys
import warnings
from os import listdir
from os.path import exists

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.decomposition import PCA
from tqdm import tqdm

warnings.filterwarnings("ignore")


def get_pca(hidden, hidden_data_path):

    """
    Extracts pca result for each hidden layer

    :param hidden: list of hidden data
    :param hidden_data_path: PATH to hidden data

    :return: pca result for each hidden layer
    """

    pca = pd.DataFrame()

    print("Start to calculate the PCA of each hidden layer.")
    for i in tqdm(hidden):
        X = pd.read_csv(
            hidden_data_path + i,
            sep=" ",
            header=None,
        )

        X_pca = PCA(n_components=1).fit_transform(X)
        pca = pd.concat([pca, pd.DataFrame(X_pca)], axis=1)

    pca.columns = [i.split(".")[0] for i in hidden]

    return pca


def get_figure(PREFIX, importance, pubchem_id):

    """
    Draws the figure of importance of each GO term

    :param PREFIX: prefix of the figure, pos or neg
    :param importance: importance of each GO term
    :param pubchem_id: pubchem id of the molecule which you want to draw the figure
    """

    print("Start to draw the figure of importance of each GO term.")
    print("Pubchem ID: {}".format(pubchem_id))
    print("Prefix: {}".format(PREFIX))
    print("Top 10 GO terms: {}".format(importance.index[:10]))
    plt.bar(list(importance.index)[:10], importance[0][:10])
    plt.xticks(rotation=45)
    plt.xlabel("Top 10 GO terms")
    plt.ylabel("PC1 score")
    plt.savefig("./{}_top10_{}.png".format(PREFIX, pubchem_id))
    plt.show()

    print("Bottom 10 GO terms: {}".format(importance.index[-10:]))
    plt.bar(list(importance.index)[-10:], importance[0][-10:])
    plt.xticks(rotation=45)
    plt.xlabel("Bottom 10 GO terms")
    plt.ylabel("PC1 score")
    plt.savefig("./{}_bottom10_{}.png".format(PREFIX, pubchem_id))
    plt.show()


def get_importance(
    hidden_data_path, test, SMILES_PubchemID_table_data_path, pubchem_id
):

    """
    Calculates the importance of each GO term using PCA

    :param hidden_data_path: PATH to hidden data
    :param test: test data
    :param SMILES_PubchemID_table_data_path: PATH to SMILES_PubchemID_table data
    :param pubchem_id: pubchem id of the molecule which you want to draw the figure

    :return: importance of each GO term and the PCA result for each hidden layer

    """

    hidden = listdir(hidden_data_path)
    hidden = [i for i in hidden if "GO" in i]

    GO_terms = get_pca(hidden, hidden_data_path)
    pubchem = pd.read_csv(SMILES_PubchemID_table_data_path, header=None, sep="\t")

    test = pd.read_csv(test, header=None, sep="\t")

    tmp = pubchem[pubchem[0] == pubchem_id]
    tmp = test[test[1] == tmp[1].values[0]]

    tmp_pos = tmp[tmp[2] > 0]
    tmp_neg = tmp[tmp[2] < 0]

    tmp_pos = pd.DataFrame(np.mean(GO_terms.loc[list(tmp_pos.index)])).sort_values(
        0, ascending=False
    )

    tmp_neg = pd.DataFrame(np.mean(GO_terms.loc[list(tmp_neg.index)])).sort_values(
        0, ascending=False
    )

    tmp_pos.to_csv("importance_for_pos_{}.csv".format(pubchem_id))
    tmp_neg.to_csv("importance_for_neg_{}.csv".format(pubchem_id))

    get_figure("pos", tmp_pos, pubchem_id)
    get_figure("neg", tmp_neg, pubchem_id)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 5:
        if exists(args[1]) and exists(args[2]) and exists(args[3]):
            get_importance(args[1], args[2], args[3], int(args[4]))
        else:
            print("Error: File not found")
    else:
        print("Looks the number of arguments is wrong.")
        print(
            "Usage: python get_GO_importance.py hidden_data_path test_data_path SMILES_PubchemID_table_data_path pubchem_id"
        )
        sys.exit(1)