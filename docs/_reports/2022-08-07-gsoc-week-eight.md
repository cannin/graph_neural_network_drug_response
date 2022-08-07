---
layout: post
title:  "Week eight | PCA, visualization, and automatic data extraction"
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
    Currently working on HP Tuning but it takes around two weeks.


2. [weight visualization](https://github.com/cannin/graph_neural_network_drug_response/issues/17)


    - [x] Visualization
      - [x] Graph Structure with PCA score
      - [x] PCA for overall hiddens
      - [x] PCA for each hidden layers    
    
3. [Train Benchmark AutoML Model](https://github.com/cannin/graph_neural_network_drug_response/issues/7)

    I run the model with only SMILES and Cell Line name as feature and it was 0.25 correlation. Then still running the model with morgan finger printing and cell2mutation data which is after using the PCA with 10 components.


4. [Understand RLIPP and implement (or use) it for describing the result with biological background ](https://github.com/cannin/graph_neural_network_drug_response/issues/19)

    Still running. This takes a week or more.

5. [Document Project Dependencies](https://github.com/cannin/graph_neural_network_drug_response/issues/8)

    Working on this one right now. I organized some files for Pipfile and r-requirement. Also set github actions for data extraction.

## Comments

  Basically current tasks are really time consuming, so plan to work in parallel, running some script and writing documents.

## Next Step

- tuning model
- autokeras
- explanation by RLIPP
- documentation

