#!/usr/bin/env python3

import os
import random
import unittest
from math import pi
from test._utils import least_used_cuda_device

import gpytorch
import torch
from gpytorch.likelihoods import BernoulliLikelihood
from gpytorch.models import AbstractVariationalGP
from gpytorch.variational import CholeskyVariationalDistribution, VariationalStrategy
from torch import optim


def train_data(cuda=False):
    train_x = torch.linspace(0, 1, 10)
    train_y = torch.sign(torch.cos(train_x * (4 * pi))).add(1).div(2)
    if cuda:
        return train_x.cuda(), train_y.cuda()
    else:
        return train_x, train_y


class GPClassificationModel(AbstractVariationalGP):
    def __init__(self, train_x):
        variational_distribution = CholeskyVariationalDistribution(train_x.size(0))
        variational_strategy = VariationalStrategy(self, train_x, variational_distribution)
        super(GPClassificationModel, self).__init__(variational_strategy)
        self.mean_module = gpytorch.means.ConstantMean()
        self.covar_module = gpytorch.kernels.ScaleKernel(gpytorch.kernels.RBFKernel())

    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        latent_pred = gpytorch.distributions.MultivariateNormal(mean_x, covar_x)
        return latent_pred


class TestSimpleGPClassification(unittest.TestCase):
    def setUp(self):
        if os.getenv("UNLOCK_SEED") is None or os.getenv("UNLOCK_SEED").lower() == "false":
            self.rng_state = torch.get_rng_state()
            torch.manual_seed(0)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(0)
            random.seed(0)

    def tearDown(self):
        if hasattr(self, "rng_state"):
            torch.set_rng_state(self.rng_state)

    def test_classification_error(self):
        train_x, train_y = train_data()
        likelihood = BernoulliLikelihood()
        model = GPClassificationModel(train_x)
        mll = gpytorch.mlls.VariationalELBO(likelihood, model, num_data=len(train_y))

        # Find optimal model hyperparameters
        model.train()
        likelihood.train()
        optimizer = optim.Adam(model.parameters(), lr=0.1)
        optimizer.n_iter = 0
        for _ in range(75):
            optimizer.zero_grad()
            output = model(train_x)
            loss = -mll(output, train_y)
            loss.backward()
            optimizer.n_iter += 1
            optimizer.step()

        for param in model.parameters():
            self.assertTrue(param.grad is not None)
            self.assertGreater(param.grad.norm().item(), 0)
        for param in likelihood.parameters():
            self.assertTrue(param.grad is not None)
            self.assertGreater(param.grad.norm().item(), 0)

        # Set back to eval mode
        model.eval()
        likelihood.eval()
        test_preds = likelihood(model(train_x)).mean.round()
        mean_abs_error = torch.mean(torch.abs(train_y - test_preds) / 2)
        assert mean_abs_error.item() < 1e-5

    def test_classification_fast_pred_var(self):
        with gpytorch.settings.fast_pred_var():
            train_x, train_y = train_data()
            likelihood = BernoulliLikelihood()
            model = GPClassificationModel(train_x)
            mll = gpytorch.mlls.VariationalMarginalLogLikelihood(likelihood, model, num_data=len(train_y))

            # Find optimal model hyperparameters
            model.train()
            likelihood.train()
            optimizer = optim.Adam(model.parameters(), lr=0.1)
            optimizer.n_iter = 0
            for _ in range(75):
                optimizer.zero_grad()
                output = model(train_x)
                loss = -mll(output, train_y)
                loss.backward()
                optimizer.n_iter += 1
                optimizer.step()

            for param in model.parameters():
                self.assertTrue(param.grad is not None)
                self.assertGreater(param.grad.norm().item(), 0)
            for param in likelihood.parameters():
                self.assertTrue(param.grad is not None)
                self.assertGreater(param.grad.norm().item(), 0)
            optimizer.step()

            # Set back to eval mode
            model.eval()
            likelihood.eval()
            test_preds = likelihood(model(train_x)).mean.round()

            mean_abs_error = torch.mean(torch.abs(train_y - test_preds) / 2)
            self.assertLess(mean_abs_error.item(), 1e-5)

    def test_classification_error_cuda(self):
        if not torch.cuda.is_available():
            return
        with least_used_cuda_device():
            train_x, train_y = train_data(cuda=True)
            likelihood = BernoulliLikelihood().cuda()
            model = GPClassificationModel(train_x).cuda()
            mll = gpytorch.mlls.VariationalMarginalLogLikelihood(likelihood, model, num_data=len(train_y))

            # Find optimal model hyperparameters
            model.train()
            optimizer = optim.Adam(model.parameters(), lr=0.1)
            optimizer.n_iter = 0
            for _ in range(75):
                optimizer.zero_grad()
                output = model(train_x)
                loss = -mll(output, train_y)
                loss.backward()
                optimizer.n_iter += 1
                optimizer.step()

            for param in model.parameters():
                self.assertTrue(param.grad is not None)
                self.assertGreater(param.grad.norm().item(), 0)
            for param in likelihood.parameters():
                self.assertTrue(param.grad is not None)
                self.assertGreater(param.grad.norm().item(), 0)
            optimizer.step()

            # Set back to eval mode
            model.eval()
            test_preds = likelihood(model(train_x)).mean.round()
            mean_abs_error = torch.mean(torch.abs(train_y - test_preds) / 2)
            self.assertLess(mean_abs_error.item(), 1e-5)


if __name__ == "__main__":
    unittest.main()
