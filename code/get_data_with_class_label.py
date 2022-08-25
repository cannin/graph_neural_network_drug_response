import random as rd

import numpy as np
import pandas as pd
from tqdm import tqdm

"""

This script is used to get the data with class label.
We just choose the data with class label DNA.

"""

# Read the data
nci60Act = pd.read_csv("../data/nci60Act_ccle.csv", index_col=0)
cell2ind = list(pd.read_table("../DrugCell/data/cell2ind.txt", header=None)[1])
nci60Act = nci60Act[list(set(cell2ind) & set(nci60Act.columns))]
nci60Act

# Make the data format for DrugCell
base = pd.DataFrame()
for i in nci60Act.columns:
    tmp = nci60Act[i].reset_index().dropna()
    tmp.columns = ["NSC", "drug_response"]
    tmp["cell_line"] = [i] * len(tmp)
    base = pd.concat([base, tmp])
base = base.reset_index(drop=True)

# Merge class and SMILES on NSC
class_nsc = pd.read_csv("../DrugCell/data_rcellminer/class_by_nsc.csv")
base_label = base.merge(class_nsc, on="NSC")
smiles = pd.read_csv("../data/nsc_cid_smiles.csv")[["NSC", "SMILES"]]
base_smiles = base_label.merge(smiles, on="NSC").drop("NSC", axis=1)

# Choose the data with class label DNA
df_dna = base_smiles[base_smiles["MECHANISM"] == "DNA"].reset_index(drop=True)[
    ["cell_line", "SMILES", "drug_response"]
]
indexes = list(df_dna.index)
rd.Random(42).shuffle(indexes)

# Randomly split the data into train, valid and test
test = indexes[round(len(indexes) * 0.8) :]
tmp = indexes[: round(len(indexes) * 0.8)]
val = tmp[: len(test)]
train = tmp[len(test) :]

train = df_dna.iloc[train]
test = df_dna.iloc[test]
val = df_dna.iloc[val]

# Save the data
test.to_csv(
    "../DrugCell/data_rcellminer/test_DNA.txt",
    sep="\t",
    header=None,
    index=None,
)

val.to_csv(
    "../DrugCell/data_rcellminer/val_DNA.txt",
    sep="\t",
    header=None,
    index=None,
)

train.to_csv(
    "../DrugCell/data_rcellminer/train_DNA.txt",
    sep="\t",
    header=None,
    index=None,
)
