---
layout: post
title:  "Week nine | PCA, visualization, and automatic data extraction"
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
    Score is 0.5


2. [weight visualization](https://github.com/cannin/graph_neural_network_drug_response/issues/17)
    Working on calculating importance of each hidden layers
    
3. [Train Benchmark AutoML Model](https://github.com/cannin/graph_neural_network_drug_response/issues/7)

    Tuning by autokeras.
    Score was 0.22.

4. [Understand RLIPP and implement (or use) it for describing the result with biological background ](https://github.com/cannin/graph_neural_network_drug_response/issues/19)

    RLIPP takes 30 months. So, I won't use original one and implemented something.

5. [Document Project Dependencies](https://github.com/cannin/graph_neural_network_drug_response/issues/8)

    Working on this one right now. I organized some files for Pipfile and r-requirement. Also set github actions for data extraction.

## Comments

    Using classes' label, I removed others data and use it for autokeras and HPTuning.  
    This reduce the time to run. 
    Also, I tried to calculate the importance of each GO term. 
    I talked with the author of RLIPP and the importance calculation is highly effected by the number of cell lines for each drugs.
    In this case, our data is too small for that and got the same score for all GO terms.
    To prevent this, running new model with large the number of hidden layers.
    I hope to show more good results and get some explanation for that.

## Next Step

- Explain by biological phenomena.
- Documentation

