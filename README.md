# Pipeline from rcellminer to DrugCell, explainable VNN model for drug response.

This is a set of scripts to get data from rcellminer, convert the data for DrugCell, run DrugCell, and get the results.

## Procedure

### 1. Extraction data using rcellminer.

```console
Rscript code/data_extraction.r
```

This is the script to get 
- relationships between PubChemID and Cell Line
- PubChemID
- drug response between Cell Lines and Drug

You can modify here to get any data what you want.

```R
nci60Act <- exprs(getAct(drugData))
```

### 2. Replace Cell Line name from nci60 to CCLE

```console
python nci60_to_ccle.py ../data/nci60Act.csv
```

This is a script that replaces the nci60 Cell Line name with the CCLE one.

### 3. Test data extraction

```console
python testdata_extraction.py ../data/PubChemIDToSmiles.csv ../data/PubChemID.csv ../data/nci60Act_ccle.csv
```

This is the script to get test data.
This requires these files:
- PubChemIDToSmiles.csv
  - Relation table between PubChemID and SMILES.
  - You can get this from [here](https://pubchem.ncbi.nlm.nih.gov/idexchange/idexchange.cgi) with PubChemID file from Step 1.
- ../data/PubChemID.csv 
- ../data/nci60Act_ccle.csv
  - These files are from step 1.

### 4. Run DrugCell model

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cannin/graph_neural_network_drug_response/blob/main/notebook/Run_DrugCell_Model_for_CellMinerCDB_Data.ipynb)


```console
git clone git@github.com:inoue0426/DrugCell.git
unzip ./DrugCell/MODEL/model.pt.zip
mkdir Hidden
mkdir Result
python code/predict_drugcell.py -gene2id ./DrugCell/data/gene2ind.txt \
                                -cell2id ./DrugCell/data/cell2ind.txt \
                                -drug2id ./DrugCell/data/drug2ind_rcell.txt \
                                -genotype ./DrugCell/data/cell2mutation.txt \
                                -fingerprint ./DrugCell/data/mfp.txt \
                                -predict ../data/rcellminer_test.txt \
                                -hidden ./Hidden \
                                -result ./Result \
                                -load ./DrugCell/MODEL/model.pt
```

This is the script to run DrugCell model.
This requires these files:
- from DrugCell repository
  - ./DrugCell/data/gene2ind.txt : index to each gene
  - ./DrugCell/data/cell2ind.txt : index to each cell line
  - ./DrugCell/data/drug2ind_rcell.txt : index to each drug
  - ./DrugCell/data/cell2mutation.txt : matrix of cell by mutations
  - ./DrugCell/data/mfp.txt : morgan finger printing for each drug
  - ./DrugCell/MODEL/model.pt : pre-trained model for rcellminer 
- from this repository
  - ../data/rcellminer_test.txt : test data 
- output directories
  - ./Hidden : directory for final hidden layers' weights 
  - ./Result : directory for each GO's correlation

### 5. (Optional) Hyper parameter tuning

```console
python ./DrugCell/code/hyperparameter_tuning.py
```

This does not require anything but you can set any parameter like -test ../data/rcellminer_test.txt.
This will return a CSV file that summarizes loss and parameters.
From this result, you can decide on hyperparameters.
