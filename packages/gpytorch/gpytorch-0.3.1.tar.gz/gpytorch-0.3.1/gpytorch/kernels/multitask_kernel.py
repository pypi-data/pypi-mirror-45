#!/usr/bin/env python3

from .kernel import Kernel
from .index_kernel import IndexKernel
from ..lazy import lazify, KroneckerProductLazyTensor


class MultitaskKernel(Kernel):
    """
    Kernel supporting Kronecker style multitask Gaussian processes (where every data point is evaluated at every
    task) using :class:`gpytorch.kernels.IndexKernel` as a basic multitask kernel.

    Given a base covariance module to be used for the data, :math:`K_{XX}`, this kernel computes a task kernel of
    specified size :math:`K_{TT}` and returns :math:`K = K_{TT} \otimes K_{XX}`. as an
    :obj:`gpytorch.lazy.KroneckerProductLazyTensor`.

    Args:
        data_covar_module (:obj:`gpytorch.kernels.Kernel`):
            Kernel to use as the data kernel.
        num_tasks (int):
            Number of tasks
        batch_size (int, optional):
            Set if the MultitaskKernel is operating on batches of data (and you want different
            parameters for each batch)
        rank (int):
            Rank of index kernel to use for task covariance matrix.
        task_covar_prior (:obj:`gpytorch.priors.Prior`):
            Prior to use for task kernel. See :class:`gpytorch.kernels.IndexKernel` for details.
    """

    def __init__(self, data_covar_module, num_tasks, rank=1, task_covar_prior=None, **kwargs):
        """
        """
        super(MultitaskKernel, self).__init__(**kwargs)
        self.task_covar_module = IndexKernel(
            num_tasks=num_tasks, batch_shape=self.batch_shape, rank=rank, prior=task_covar_prior
        )
        self.data_covar_module = data_covar_module
        self.num_tasks = num_tasks

    def forward(self, x1, x2, diag=False, last_dim_is_batch=False, **params):
        if last_dim_is_batch:
            raise RuntimeError("MultitaskKernel does not accept the last_dim_is_batch argument.")
        covar_i = self.task_covar_module.covar_matrix
        if len(x1.shape[:-2]):
            covar_i = covar_i.repeat(*x1.shape[:-2], 1, 1)
        covar_x = lazify(self.data_covar_module.forward(x1, x2, **params))
        res = KroneckerProductLazyTensor(covar_x, covar_i)
        return res.diag() if diag else res

    def num_outputs_per_input(self, x1, x2):
        """
        Given `n` data points `x1` and `m` datapoints `x2`, this multitask
        kernel returns an `(n*num_tasks) x (m*num_tasks)` covariancn matrix.
        """
        return self.num_tasks
