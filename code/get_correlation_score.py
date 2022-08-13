import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")

from os import listdir

from joblib import Parallel, delayed
from scipy.stats import spearmanr
from sklearn.linear_model import RidgeCV
from tqdm import tqdm

test = pd.read_csv("../DrugCell/data_rcellminer/test_rcell.txt", header=None, sep="\t")


def get_list(i):

    """
    Gets the list of GO terms

    :param i: index of the Drug

    :return: list of GO terms
    """

    tmp = test[test[1] == i]
    return [
        len(tmp[2]),
        tmp.index[0],
        list(tmp[2]),
        list(test[test[1] == i][1])[0],
    ]


t = Parallel(n_jobs=-1)(delayed(get_list)(i) for i in tqdm(set(test[1])))
t = pd.DataFrame(t).sort_values(0)
t = t[t[0] > 9]
t = t[[1, 2, 3]].reset_index(drop=True)
t.columns = ["drug_index", "drug_response", "drug"]


def get_corr(GO, t):
    """
    Gets the correlation between the predicted response and the actual response of the drug
    Drug response is predicted by the ridge regression model for each GO term of hidden layer
    Then checks the correlation for all drugs for each GO term of hidden layer

    :param GO: list of GO terms
    :param t: list of drugs
    """
    hidden = pd.read_csv(
        "/export/scratch/inoue019/Hidden_157/" + GO, header=None, sep=" "
    )

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
