import sys
from os import listdir
from os.path import exists

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from tqdm import tqdm


def get_pca_result(test_data_path, hidden_data_path):
    p = pd.read_csv(test_data_path, header=None, sep="\t")

    hidden = listdir(hidden_data_path)
    hidden = [i for i in hidden if "GO" in i]

    X = pd.DataFrame()
    for i in tqdm(hidden):
        X = pd.concat(
            [X, pd.read_table(hidden_data_path + i, sep=" ", header=None)],
            axis=1,
        )

    X.columns = list(range(X.shape[1]))
    X_pca = PCA(n_components=2).fit_transform(X)

    f, ax = plt.subplots()
    points = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=p[2], cmap="coolwarm")

    ax.set_xlabel("PC1", fontsize=15)
    ax.set_ylabel("PC2", fontsize=15)

    f.colorbar(points)

    plt.show()
    plt.savefig("pca_result.png")


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        if exists(args[1]) and exists(args[2]):
            get_pca_result(args[1], args[2])
        else:
            print("Error: File not found")
    else:
        print("Looks the number of arguments is wrong.")
        print(
            "Usage: python get_pca_result.py test_data_path hidden_data_path pca_result_path"
        )
        sys.exit(1)
