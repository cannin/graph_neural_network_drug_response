import networkx as nx
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem

train = pd.read_csv(
    "../DrugCell/data_rcellminer/train_DNA.txt", header=None, sep="\t"
)

pd.DataFrame(set(train[1])).reset_index().to_csv(
    "../DrugCell/data_rcellminer/drug2ind.txt",
    sep="\t",
    header=None,
    index=None,
)

mfp = np.array(
    [
        np.array(
            AllChem.GetMorganFingerprintAsBitVect(
                Chem.MolFromSmiles(i), useChirality=True, radius=2, nBits=2048
            )
        )
        for i in set(train[1])
    ]
)

pd.DataFrame(mfp).to_csv(
    "../DrugCell/data_rcellminer/drug2fingerprint.csv",
    sep=",",
    header=None,
    index=None,
)

pd.DataFrame(set(train[0])).reset_index().to_csv(
    "../DrugCell/data_rcellminer/cell2ind.txt",
    header=None,
    index=None,
    sep="\t",
)

cell2ind = pd.read_csv("../DrugCell/data/cell2ind.txt", header=None, sep="\t")

t = pd.read_csv(
    "../DrugCell/data_rcellminer/cell2ind.txt", header=None, sep="\t"
)

cell2mut = (
    pd.read_csv(
        "../DrugCell/data/cell2mutation.txt",
        header=None,
    )
    .loc[[int(cell2ind[cell2ind[1] == i][0]) for i in t[1]]]
    .reset_index(drop=True)
)

none_zero_cols = list(np.sum(cell2mut) != 0)
cell2mut = cell2mut.loc[:, none_zero_cols]
cell2mut = cell2mut.T.reset_index(drop=True).T
cell2mut.to_csv(
    "../DrugCell/data_rcellminer/cell2mut.txt",
    header=None,
    index=None,
)

gene2ind = pd.read_csv("../DrugCell/data/gene2ind.txt", header=None, sep="\t")
gene2ind = gene2ind.loc[none_zero_cols]
gene2ind = pd.DataFrame(list(gene2ind[1]))
gene2ind.to_csv(
    "../DrugCell/data_rcellminer/gene2ind.txt", header=None, sep="\t"
)

graph = pd.read_csv("../DrugCell/data/drugcell_ont.txt", header=None, sep="\t")
gene = graph[graph[2] == "gene"]

g = pd.DataFrame()
for i in gene2ind[0]:
    g = pd.concat([g, gene[gene[1] == i]])

go = pd.concat([graph[graph[2] == "default"], g])

go.reset_index(drop=True).to_csv(
    "../DrugCell/data_rcellminer/go.txt", header=None, sep="\t", index=None
)
