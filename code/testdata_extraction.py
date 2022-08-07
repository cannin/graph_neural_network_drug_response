import sys

import numpy as np
import pandas as pd


def extractTestData(SMILES, nci60PubChemID, nci60Act_ccle):

    # Read original train data
    train = pd.read_table("./data/drugcell_train.txt", header=None)

    # Get SMILES from PubChem ID  https://pubchem.ncbi.nlm.nih.gov/idexchange/idexchange.cgi
    smiles = pd.read_table(SMILES, header=None).drop(0, axis=1)

    # Replace index with Drug ID
    smiles.index = pd.read_csv(nci60PubChemID, index_col=0).index
    smiles.columns = ["SMILES"]

    # Check if the SMILES are in the train data
    t = pd.DataFrame()
    for i in smiles["SMILES"]:
        if len(train[train[1] == i]) > 0:
            t = pd.concat([t, smiles[smiles["SMILES"] == i]])

    smiles = t.copy()

    # Choose the columns and indexes that are in the train data
    nci60Act = pd.read_csv(nci60Act_ccle, index_col=0)
    nci60Act = nci60Act.loc[sorted(list(set(smiles.index) & set(nci60Act.index)))][
        list(set(train[0]) & set(nci60Act.columns))
    ]

    # Adjust data structure to match the train data
    test = pd.DataFrame()
    for i in nci60Act.columns:
        tmp = pd.DataFrame((nci60Act[i].dropna()))
        tmp.columns = ["Drug Response"]
        tmp["Cell Line"] = [i] * len(tmp)
        tmp = pd.merge(tmp, smiles, left_index=True, right_index=True)
        test = pd.concat([test, tmp])

    test = test[["Cell Line", "SMILES", "Drug Response"]]
    test = test.reset_index(drop=True)

    test.to_csv("../data/rcellminer_test.txt", sep="\t", header=None, index=None)


if __name__ == "__main__":
    # require file PATH as an argument
    args = sys.argv

    if len(args) == 4:
        extractTestData(args[1], args[2], args[3])
    else:
        print(
            "Argument Error: Requires 3 arguments, SMILES, PubChemID and nci60Act_ccle"
        )
