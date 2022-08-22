---
layout: post
title:  "Week ten | Retraining and visualization"
tags: gsoc
author: Yoshitaka Inoue
---

## GSoC Project

- [GSoC Project URL](https://summerofcode.withgoogle.com/programs/2022/projects/ylOolPrk)
- [Work Repository](https://github.com/cannin/graph_neural_network_drug_response)

Mentor:
**Augustin Luna** ([@cannin](https://github.com/cannin))

## Tasks

1. [Re-train DrugCell model](https://github.com/cannin/graph_neural_network_drug_response/issues/13).  
    Done HP tuning for small data, without the label of Other
    Score is 0.67.

2. [weight visualization](https://github.com/cannin/graph_neural_network_drug_response/issues/17)
    I've got the correlation score for GO terms and genes.
    Also add some visualization and explain some drugs.

3. [Document Project Dependencies](https://github.com/cannin/graph_neural_network_drug_response/issues/8)

    Working on modifying README.

4. [create datasets for rcellminer](https://github.com/cannin/graph_neural_network_drug_response/issues/21)

For retraining, I've created new file for inputs, cell2ind, drug2ind, and drug2fingerprint.

## Comments

Currently working on explaining drugs and correlation from biological phenomena.  
Some important GO terms are missing, so it might be challenging to explain whole drugs.  
So, I plan to focus on some specific drugs approved by the FDA.  
I still need to improve the model, so I will do experiments in parallel.  

In addition, I've been extracting SMILES data from PubChem ID in rcellminer because I used to use the drug2id from original data.   
But right now I've created new drug2ind exclusive for our data. So, I can use our own PubChem data directly.   
I'll try this after current experiments.  

## Next Step

- Explain by biological phenomena.
- Documentation
- add comments
- retraining

