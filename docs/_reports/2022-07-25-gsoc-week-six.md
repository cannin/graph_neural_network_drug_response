---
layout: post
title:  "Week six | weight visualization"
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
    Status: **Done**.   
    Branch: **[6-drugcell-test](https://github.com/cannin/graph_neural_network_drug_response/tree/6-drugcell-test)**.  
    PR: **None**.
    
    Retrain model. The score was 0.35 and right now try to change paramters and rerun it.

2. [weight visualization](https://github.com/cannin/graph_neural_network_drug_response/issues/17)

  visualize weight differences. Apparently there are some difference between cell lines. 
  But understanding difference in detail is still difficult.
  

## Comments

This week, we have retrained and visualized the weights. So far the correlation is 0.35, which is not good.  
I would like to get at least 0.6. IMO, the main issue is the amount of data. (The combination of Cell Line and Drug is not so large.)  
Therefore, the accuracy may be improved by selecting data, hyper-parameter tuning, and so on.
With less than a month to go, I will do more experiments asap.

## Next Step

- tuning model
- talking with the author of DrugCell
- remove some data which is not sufficient for the model
