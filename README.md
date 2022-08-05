# Pipeline from rcellminer to DrugCell, explainable VNN model for drug response.

This is a set of scripts to get data from rcellminer, convert the data for DrugCell, run DrugCell, and get the results.

## Computational environment

Ubuntu version: 20.04.4 LTS  
GPU spec: GeForce RTX 3080    
Python version: 3.9.5    
R version: 4.1.3   

### Python requirement
- torch 
- networkx 
- pandas 
- numpy 
- scipy
- scikit-learn
- rdkit-pypi 
- (optional) optuna

### R requirement
- BiocManager
- rcellminer

*** You can also check [dockerfile](https://github.com/cannin/graph_neural_network_drug_response/blob/main/Dockerfile)

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


### 5. Visualization using Cytoscape and PCA

```console
<!-- get PCA result -->
python get_pca_result.py  DrugCell/data/rcellminer_test.txt /PATH/To/Hidden/
<!-- get graph structure -->
python get_graph_structure.py SAMPLE_INDEX /PATH/To/Hidden/ DrugCell/data/drugcell_ont.txt
```

This is the script to get visualizatian and graph structure.
This requires these files:
- from DrugCell repository
  - DrugCell/data/drugcell_ont.txt : ontology relationships data
- from this repository
  - ../data/rcellminer_test.txt : test data 
- from DrugCell prediction output
  - /PATH/To/Hidden/ : directory for final hidden layers' weights 
- from user's focus
  - SAMPLE_INDEX : this is the indexes to samples in test data which user focus on. (Ex. "100,200")

When you run the get_pca_result.py, this concatenates all GO:XXXXXX.hidden for each sample and then runs PCA.
So if you run it, you can get a figure as below. Coloring is based on drug response.


![pca_result](https://user-images.githubusercontent.com/8393063/182660161-41039436-131a-4a94-bd3f-ac48381f4278.png)


When you run the get_graph_structure.py, you can get graph.csv and weight.csv.   
This requires sample indexes like "100,200,300". This means that from the test data, this code picks up sample indexes 100, 200, and 300 and then calculates the weight of each sample.
Concretely, we first construct a graph structure based on Gene Ontology. The data contains GO and gene information and is saved as graph.csv.
Next, this obtains weights for each sample from the hidden layer. For example, for three samples of 100, 200, and 300, we obtain weights for 2068 nodes (GOs).
Here, since the weights of the genes are not included in the hidden layer, we need to calculate them somehow. To do this, this code first enumerates all the ways to GO:0008150 from each gene. Then add up all the weights of each Gene Ontology we pass when going to GO:0008150, which we defined as the weight for each gene.

The following is a visualization using Cytoscape.

![Screen Shot 2022-07-24 at 12 56 20](https://user-images.githubusercontent.com/8393063/182660299-e9c755f1-31c7-4b91-a38e-8a853f7ef712.png)

### 6. Identification of subsystems important using RLIPP

```console

git clone https://github.com/aksinghal5590/rlipp.git
cd rlipp
sh  scripts/rlipp.sh 
```

This is the method that is officially used in the DrugCell paper.  
You need to modify scripts/rlipp.sh to adjust to your environment.

In this script, ridge regression is performed based on the results of the hidden layer of each GO to produce correlations. By comparing this correlation with the correlation of the parent, RLIPP is computed. Positive RLIPP indicates higher predictive power than children, while negative values indicate low predictive power.       
  
  
  
$$
\text{RLIPP score} = \left(\rho_{2}-\rho_{1}\right) / \rho_{1},
$$

where $\rho_{1}$ is children's correlation and $\rho_{2}$ is parent's correlation.

### 7. (Optional) Hyper parameter tuning

```console
python ./DrugCell/code/hyperparameter_tuning.py
```

This does not require anything but you can set any parameter like -test ../data/rcellminer_test.txt.
This will return a CSV file that summarizes loss and parameters.
From this result, you can decide on hyperparameters.

