import argparse
import os
import sys
import time

import numpy as np
import optuna
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as du
from optuna.trial import TrialState
from torch.autograd import Variable

import util
from drugcell_NN import *
from util import *


def create_term_mask(term_direct_gene_map, gene_dim):

    term_mask_map = {}

    for term, gene_set in term_direct_gene_map.items():

        mask = torch.zeros(len(gene_set), gene_dim)

        for i, gene_id in enumerate(gene_set):
            mask[i, gene_id] = 1

        mask_gpu = torch.autograd.Variable(mask.cuda(0))

        term_mask_map[term] = mask_gpu

    return term_mask_map


def get_data():

    torch.set_printoptions(precision=5)
    train_data, cell2id_mapping, drug2id_mapping = prepare_train_data(
        "data/train_rcell_over50_not_equal.txt",
        "data/val_rcell_over50_not_equal.txt",
        "data/cell2ind.txt",
        "data/drug2ind_rcell.txt",
    )

    gene2id_mapping = load_mapping("data/gene2ind.txt")
    cell_features = np.genfromtxt("data/cell2mutation.txt", delimiter=",")
    drug_features = np.genfromtxt("data/mfp.txt", delimiter=",")

    num_cells = len(cell2id_mapping)
    num_drugs = len(drug2id_mapping)
    num_genes = len(gene2id_mapping)
    drug_dim = len(drug_features[0, :])

    dG, root, term_size_map, term_direct_gene_map = load_ontology(
        "data/drugcell_ont.txt", gene2id_mapping
    )

    num_hiddens_genotype = 6
    num_hiddens_drug = [512, 256, 64, 8]
    num_hiddens_final = 6

    return (
        root,
        term_size_map,
        term_direct_gene_map,
        dG,
        train_data,
        num_genes,
        drug_dim,
        cell_features,
        drug_features,
    )


def objective(trial):

    (
        root,
        term_size_map,
        term_direct_gene_map,
        dG,
        train_data,
        gene_dim,
        drug_dim,
        cell_features,
        drug_features,
    ) = get_data()

    train_epochs = 3

    num_hiddens_genotype = trial.suggest_int("num_hiddens_genotype", 1, 6)
    num_hiddens_final = trial.suggest_int("num_hiddens_final", 1, 6)
    i = trial.suggest_int("i", 1, 4)

    if i == 1:
        num_hiddens_drug = [256, 64, 4]
    elif i == 2:
        num_hiddens_drug = [256, 64, 8]
    elif i == 3:
        num_hiddens_drug = [512, 256, 64, 8]
    else:
        num_hiddens_drug = [512, 256, 64, 8, 4]

    model = drugcell_nn(
        term_size_map,
        term_direct_gene_map,
        dG,
        gene_dim,
        drug_dim,
        root,
        num_hiddens_genotype,
        num_hiddens_drug,
        num_hiddens_final,
    )

    train_feature, train_label, test_feature, test_label = train_data
    train_label_gpu = torch.autograd.Variable(train_label.cuda(CUDA_ID))
    test_label_gpu = torch.autograd.Variable(test_label.cuda(CUDA_ID))

    model.cuda(CUDA_ID)

    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)

    optimizer = torch.optim.Adam(
        model.parameters(), lr=lr, betas=(0.9, 0.99), eps=1e-05
    )

    term_mask_map = create_term_mask(model.term_direct_gene_map, gene_dim)
    optimizer.zero_grad()

    for name, param in model.named_parameters():
        term_name = name.split("_")[0]

        if "_direct_gene_layer.weight" in name:
            param.data = torch.mul(param.data, term_mask_map[term_name]) * 0.1
        else:
            param.data = param.data * 0.1

    batch_size = trial.suggest_categorical(
        "batch_size", [1000, 2000, 3000, 4000, 5000, 6000]
    )

    train_loader = du.DataLoader(
        du.TensorDataset(train_feature, train_label),
        batch_size=batch_size,
        shuffle=False,
    )

    for epoch in range(train_epochs):

        # Train
        model.train()
        train_predict = torch.zeros(0, 0).cuda(CUDA_ID)

        for i, (inputdata, labels) in enumerate(train_loader):
            features = build_input_vector(inputdata, cell_features, drug_features)
            cuda_features = torch.autograd.Variable(features.cuda(CUDA_ID))
            cuda_labels = torch.autograd.Variable(labels.cuda(CUDA_ID))
            optimizer.zero_grad()
            aux_out_map, _ = model(cuda_features)

            if train_predict.size()[0] == 0:
                train_predict = aux_out_map["final"].data
            else:
                train_predict = torch.cat(
                    [train_predict, aux_out_map["final"].data], dim=0
                )

            total_loss = 0
            for name, output in aux_out_map.items():
                loss = nn.MSELoss()
                if name == "final":
                    total_loss += loss(output, cuda_labels)
                else:  # change 0.2 to smaller one for big terms
                    total_loss += 0.2 * loss(output, cuda_labels)

            total_loss.backward()

            for name, param in model.named_parameters():
                if "_direct_gene_layer.weight" not in name:
                    continue
                term_name = name.split("_")[0]
                param.grad.data = torch.mul(param.grad.data, term_mask_map[term_name])

            optimizer.step()

        trial.report(total_loss, epoch)

        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    return total_loss


CUDA_ID = 0

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=3)

study.trials_dataframe().to_csv("study_history.csv")
