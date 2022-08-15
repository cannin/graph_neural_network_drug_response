import argparse
import os
import sys

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as du
import util
from drugcell_NN import *
from torch.autograd import Variable
from util import *


def predict_dcell(
    test,
    cell2id,
    drug2id,
    cell2mut,
    fingerprint,
    model,
    hidden_folder,
    result_folder,
    batch_size=1000,
):

    predict_data, _, _ = prepare_predict_data(test, cell2id, drug2id)
    # load cell/drug features
    cell_features = np.genfromtxt(cell2mut, delimiter=",")
    drug_features = np.genfromtxt(fingerprint, delimiter=",")

    model = torch.load(model, map_location=lambda storage, location: storage)

    predict_feature, predict_label = predict_data

    model.eval()

    test_loader = du.DataLoader(
        du.TensorDataset(predict_feature, predict_label),
        batch_size=batch_size,
        shuffle=False,
    )

    # Test
    test_predict = torch.zeros(0, 0)
    term_hidden_map = {}

    batch_num = 0
    for i, (inputdata, labels) in enumerate(test_loader):
        # Convert torch tensor to Variable
        features = build_input_vector(inputdata, cell_features, drug_features)

        # make prediction for test data
        aux_out_map, term_hidden_map = model(features)

        if test_predict.size()[0] == 0:
            test_predict = aux_out_map["final"].data
        else:
            test_predict = torch.cat([test_predict, aux_out_map["final"].data], dim=0)

        for term, hidden_map in term_hidden_map.items():
            this_hidden_file = hidden_folder + "/" + term + "_" + str(i) + ".txt"
            hidden_file = hidden_folder + "/" + term + ".hidden"

            np.savetxt(this_hidden_file, hidden_map.data.cpu().numpy(), "%.4e")

            # append it to one file
            os.system("cat " + this_hidden_file + " >> " + hidden_file)
            os.system("rm " + this_hidden_file)

        batch_num += 1

    test_corr = pearson_corr(test_predict, predict_label)
    print("Test pearson corr\t%s\t%.6f" % (model.root, test_corr))

    np.savetxt(result_folder + "/drugcell.predict", test_predict.numpy(), "%.4e")
