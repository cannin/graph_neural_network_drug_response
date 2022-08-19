# Pipeline from rcellminer to DrugCell, explainable VNN model for drug response.

This is a set of scripts to get data from rcellminer, convert the data for DrugCell, run DrugCell, and get the results.

## Procedure

* Step 1-3 are automatically running by GitHub actions. You can use each scripts if you want to run manually.   
* You can get the artifact from [here](https://github.com/cannin/graph_neural_network_drug_response/actions/workflows/data_extraction.yml).

### 1. Extraction data using rcellminer.

<details>

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
</details>


### 2. Replace Cell Line name from nci60 to CCLE

<details>

```console
python nci60_to_ccle.py ../data/nci60Act.csv
```

This is a script that replaces the nci60 Cell Line name with the CCLE one.

</details>

### 3. Test data extraction

<details>

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

</details>

### 4. Run DrugCell model

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cannin/graph_neural_network_drug_response/blob/main/notebook/Run_DrugCell_Model_for_CellMinerCDB_Data.ipynb)

```console
git clone git@github.com:inoue0426/DrugCell.git
unzip ./DrugCell/MODEL/model.pt.zip
mkdir Hidden
mkdir Result
python code/predict_drugcell.py -gene2id ./DrugCell/data_rcellminer/gene2ind.txt \
                                -cell2id ./DrugCell/data_rcellminer/cell2ind.txt \
                                -drug2id ./DrugCell/data_rcellminer/drug2ind.txt \
                                -genotype ./DrugCell/data_rcellminer/cell2mut.txt \
                                -fingerprint ./DrugCell/data_rcellminer/drug2fingerprint.csv \
                                -predict ./DrugCell/data_rcellminer/test_rcell_wo_other.txt \
                                -hidden ./Hidden \
                                -result ./Result \
                                -load ./DrugCell/pretrained_model_rcellminer/model.pt
```

[DrugCell's document](https://github.com/inoue0426/DrugCell#drugcell-release-v10)

### 5 Get corralation score for each GO Term
  
- [get_correlation_score.ipynb](https://github.com/cannin/graph_neural_network_drug_response/blob/main/notebook/get_correlation_score.ipynb)

This is implemented based on RLIPP, the evaluation function for DrugCell. [github](https://github.com/aksinghal5590/rlipp)
  
Based on the correlation, this code interprets which GO is effective for each drug. The Hidden Layer's value is first obtained for each drug's GO. A ridge regression is performed using this as the feature value and DrugCell's predicted value as y. Afterwards, the predicted value is compared with the predicted value in DrugCell. The correlation between this predicted value and the predicted value of DrugCell helps us determine how well the hidden layer of this GO is performing.
  
### 6. Visualization using Cytoscape and PCA

- [get_pca_result.ipynb](https://github.com/cannin/graph_neural_network_drug_response/blob/main/notebook/get_pca_result.ipynb)
- [get_graph_structure.ipynb](https://github.com/cannin/graph_neural_network_drug_response/blob/main/notebook/get_graph_structure.ipynb)
- [get_GO_importance.ipynb](https://github.com/cannin/graph_neural_network_drug_response/blob/main/notebook/get_GO_importance.ipynb)

```console
<!-- get PCA result -->
python code/get_pca_result.py  DrugCell/data/rcellminer_test.txt /PATH/To/Hidden/
<!-- get graph structure -->
python code/get_graph_structure.py SAMPLE_INDEX /PATH/To/Hidden/ DrugCell/data/drugcell_ont.txt
<!-- get GO importance using PCA -->
python code/get_GO_importance.py /PATH/To/Hidden/ ./DrugCell/data/test_rcell_over50_not_equal.txt ./DrugCell/data/SMILES_from_PubchemID.txt PUBCHEM_ID
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

When you run get_GO_importance, you can get importance_for_pos_DRUG_INDEX.csv and importance_for_neg_DRUG_INDEX.csv table.
In addition this return below figures, first two pics are figure of top 10 PC1 score GO and bottom10 for positive drug responce score's Cell Line and others are for negative drug responce score's Cell Line.
  
This script's first step is applying PCA to all Hidden Layer values with n_compounds = 1. There are 2000 GOs and 100,000 samples, so a matrix of 100,000*2000 is generated.

Next step is determining which cell line contains the drug based on the Pubchem ID. Since this data has a Drug Response value, it is divided into Positive and Negative data, depending on whether it is greater or equal to 0.

The PCA values for each GO are then averaged for Positives and Negatives. The Top10 and Bottom10 are sorted and saved for each Positive and Negative.

![image](https://user-images.githubusercontent.com/8393063/183324468-1b1f5150-a402-4922-8b30-d5c04b1e3c5a.png)

![image](https://user-images.githubusercontent.com/8393063/183324471-a8a52391-f109-4caf-8f34-0600a0527e21.png)

![image](https://user-images.githubusercontent.com/8393063/183324479-ce51ecb9-d18f-4f4a-a79b-3ff918901fdb.png)

![image](https://user-images.githubusercontent.com/8393063/183324491-7d6cfb16-124f-4081-8e0c-0955b97db8e4.png)
  
### 6. (Optional) Hyper parameter tuning

<details>

```console
python ../DrugCell/code/hyperparameter_tuning.py
```

This does not require anything but you can set any parameter like -test ../data/rcellminer_test.txt.
This will return a CSV file that summarizes loss and parameters.
From this result, you can decide on hyperparameters.

</details>
