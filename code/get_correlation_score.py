import sys
import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")

from os import listdir

from joblib import Parallel, delayed
from sklearn.linear_model import RidgeCV
from tqdm import tqdm


def get_list(i, test):
    """
    Gets the list of GO terms

    :param i: index of the Drug
    :param test: dataframe of test data

    :return: list of GO terms
    """

    tmp = test[test[1] == i]
    return [
        len(tmp[2]),
        tmp.index[0],
        list(tmp[2]),
        list(test[test[1] == i][1])[0],
    ]


def get_corr(go_dir_path, GO, t):
    """
    Gets the correlation between the predicted response and the actual response of the drug
    Drug response is predicted by the ridge regression model for each GO term of hidden layer
    Then checks the correlation for all drugs for each GO term of hidden layer

    :param GO: list of GO terms
    :param t: list of drugs
    """
    hidden = pd.read_csv(go_dir_path + GO, header=None, sep=" ")

    drug_index = list(t["drug_index"])

    corr = []
    for i, j in enumerate(drug_index):
        y = t["drug_response"][i]
        X = np.tile(list(hidden.iloc[j]), (len(y), 1))

        regr = RidgeCV(cv=3)
        regr.fit(X, y)
        y_pred = regr.predict(X)
        corr.append(np.correlate(y, y_pred)[0])

    return corr


def get_corr_parallel(go_dir_path, test_data_path, smiles_pubchem_path):

    """
    Gets the correlation between the predicted response and the actual response of the drug

    :param go_dir_path: path to the directory of GO terms
    :param test_data_path: path to the test data
    :param smiles_pubchem_path: path to the smiles and pubchem data

    :return: correlation between the predicted response and the actual response of the drug
    """

    test = pd.read_csv(test_data_path, header=None, sep="\t")
    t = Parallel(n_jobs=-1)(delayed(get_list)(i, test) for i in tqdm(set(test[1])))
    t = pd.DataFrame(t).sort_values(0)
    t = t[t[0] > 9]
    t = t[[1, 2, 3]].reset_index(drop=True)
    t.columns = ["drug_index", "drug_response", "drug"]

    hidden = listdir(go_dir_path)
    hidden = [i for i in hidden if "GO" in i]

    p = Parallel(n_jobs=-1)(delayed(get_corr)(go_dir_path, i, t) for i in tqdm(hidden))

    pubchem_id = pd.read_csv(
        smiles_pubchem_path,
        header=None,
        sep="\t",
    )
    pubchem_id = {pubchem_id[1][i]: pubchem_id[0][i] for i in pubchem_id.index}

    pd.DataFrame(
        p,
        index=[i.split(".")[0] for i in hidden],
        columns=[pubchem_id[i] for i in list(t["drug"])],
    ).to_csv("correlation_score.csv")


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 4:
        go_dir_path = args[1]
        test_data_path = args[2]
        smiles_pubchem_path = args[3]
        get_corr_parallel(go_dir_path, test_data_path, smiles_pubchem_path)
    else:
        print("Looks the number of arguments is wrong.")
