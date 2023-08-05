#!/usr/bin/env python3

import unittest
import torch
from gpytorch.likelihoods import BernoulliLikelihood
from gpytorch.likelihoods import Likelihood
from test.likelihoods._base_likelihood_test_case import BaseLikelihoodTestCase


class TestBernoulliLikelihood(BaseLikelihoodTestCase, unittest.TestCase):
    seed = 0

    def _create_targets(self, batch_shape=torch.Size([])):
        res = torch.randn(*batch_shape, 5).gt(0).float()
        return res

    def _test_log_prob(self, batch_shape):
        # Overwriting this because use use probit, not logit
        # The values are close, but not exact
        # So we use looser checks
        likelihood = self.create_likelihood()
        input = self._create_marginal_input(batch_shape)
        target = self._create_targets(batch_shape)
        output = likelihood.expected_log_prob(target, input)

        self.assertTrue(torch.is_tensor(output))
        self.assertEqual(output.shape, batch_shape)
        default_log_prob = Likelihood.expected_log_prob(likelihood, target, input)
        self.assertAllClose(output, default_log_prob, rtol=0.25, atol=0.1)

    def create_likelihood(self):
        return BernoulliLikelihood()
