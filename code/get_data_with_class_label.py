import random as rd

import numpy as np
import pandas as pd
from tqdm import tqdm

# Create PubChem_id list
pubchem_id = pd.read_csv(
    "DrugCell/data_rcellminer/pubchem_id_by_nsc.csv", index_col=0
).dropna()
pubchem_id


smiles = pd.read_table(
    "DrugCell/data_rcellminer/SMILES_from_PubchemID.txt", header=None
)
smiles.index = pubchem_id.index
smiles = smiles.drop(0, axis=1)
smiles.columns = ["smiles"]
smiles = smiles.to_dict()["smiles"]


nci60Act = pd.read_csv("data/nci60Act_ccle.csv", index_col=0)
cell2ind = list(pd.read_table("DrugCell/data/cell2ind.txt", header=None)[1])
nci60Act = nci60Act[list(set(cell2ind) & set(nci60Act.columns))]


base = pd.DataFrame()
for i in nci60Act.columns:
    tmp = nci60Act[i].reset_index().dropna()
    tmp.columns = ["nsc", "drug_response"]
    tmp["cell_line"] = [i] * len(tmp)
    base = pd.concat([base, tmp])


class_nsc = pd.read_csv(
    "DrugCell/data_rcellminer/class_by_nsc.csv",
)


class_nsc["MECHANISM"].value_counts()


nsc_list = set(class_nsc["NSC"])
class_nsc = {class_nsc["NSC"][i]: class_nsc["MECHANISM"][i] for i in class_nsc.index}


base["label"] = [class_nsc[i] if i in nsc_list else None for i in base["nsc"]]
base = base[base["label"] != "Other"].reset_index(drop=True).drop("label", axis=1)
base["smiles"] = [smiles[i] if i in smiles.keys() else None for i in base.nsc]
base = base.dropna()
base = base.reset_index(drop=True)
base = base[["cell_line", "smiles", "drug_response"]]


indexes = list(base.index)
rd.Random(42).shuffle(indexes)


test = indexes[round(len(indexes) * 0.8) :]
tmp = indexes[: round(len(indexes) * 0.8)]
val = tmp[: len(test)]
train = tmp[len(test) :]


train = base.iloc[train]
test = base.iloc[test]
val = base.iloc[val]


df = pd.merge(
    pd.merge(
        pd.DataFrame(train["cell_line"].value_counts()),
        pd.DataFrame(val["cell_line"].value_counts()),
        left_index=True,
        right_index=True,
    ),
    pd.DataFrame(test["cell_line"].value_counts()),
    left_index=True,
    right_index=True,
)
df.columns = ["train", "val", "test"]
df.loc["total"] = np.sum(df, axis=0)


test.to_csv(
    "DrugCell/data_rcellminer/test_rcell_wo_other.txt",
    sep="\t",
    header=None,
    index=None,
)

val.to_csv(
    "DrugCell/data_rcellminer/val_rcell_wo_other.txt",
    sep="\t",
    header=None,
    index=None,
)

train.to_csv(
    "DrugCell/data_rcellminer/train_rcell_wo_other.txt",
    sep="\t",
    header=None,
    index=None,
)
