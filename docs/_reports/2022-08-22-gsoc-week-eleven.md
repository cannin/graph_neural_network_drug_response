---
layout: post
title:  "Week eleven | Wrap up for final week"
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
    Done HP tuning for small data, only focus on DNA
    Score is 0.71.

2. [weight visualization](https://github.com/cannin/graph_neural_network_drug_response/issues/17)
    I've got the correlation score for GO terms and genes.
    Also add some visualization and explain some drugs.

3. [Document Project Dependencies](https://github.com/cannin/graph_neural_network_drug_response/issues/8)

    Working on modifying README.

## Comments

I've created the explanation of some drugs and it can be evaluated by some papers. So, this might be shown that our model can explain some drugs' relationship with GO term correctly. For the next step, I will dig into more from genes. Although I don't have so much time...

## Next Step

- Documentation
- add comments
- Calculate top 20's GO term
