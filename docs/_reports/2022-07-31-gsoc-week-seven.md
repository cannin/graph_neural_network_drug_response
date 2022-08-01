---
layout: post
title:  "Week seven | still working on visualization and hptuning"
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
    Status: **WIP**.   
    Branch: **[6-drugcell-test](https://github.com/cannin/graph_neural_network_drug_response/tree/6-drugcell-test)**.  
    PR: **None**.
    
    Retrain model. The score was 0.46 and right now try to hyperparameter tuning.

2. [weight visualization](https://github.com/cannin/graph_neural_network_drug_response/issues/17)
    Status: **WIP**.   
    Branch: **[17-weight-visualization](https://github.com/cannin/graph_neural_network_drug_response/tree/17-weight-visualization)**.  
    PR: **None**.

    From the last meeting with the author of DrugCell, probably I can show the Fig 3 from original paper using PCA.
    But this is not so informative and to show some biological explain from result, probably graph structure is better.
    Or calculating something importance from weight, not sure how to do that right now though.
    
3. add comments for pipeline
    I just updated the README to use the pipeline from data extraction to running the DrugCell.   
    
    
## Comments

Still struggling to show the biological background for the model's result.    
Probably I only need to show some examples, so I'll focus on some specific Cell Line, Drug, and GO, and from these relationships, I want to explore explainable phenomena.

## Next Step

- tuning model
- visualization
- explanation the model

