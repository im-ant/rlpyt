
import torch

from rlpyt.distributions.base import Distribution
from rlpyt.distributions.discrete import DiscreteMixin


class EpsilonGreedy(DiscreteMixin, Distribution):
    """Input can be shaped [T,B,Q] or [B,Q], and vector epsilon of length
    B will apply across the Batch dimension (same epsilon for all T)."""

    def __init__(self, epsilon=1, **kwargs):
        super().__init__(**kwargs)
        self._epsilon = epsilon

    def sample(self, q):
        arg_select = torch.argmax(q, dim=-1)
        rand_mask = torch.rand(arg_select.shape) < self._epsilon
        arg_rand = torch.randint(low=0, high=q.shape[-1],
            size=(rand_mask.sum(),))
        arg_select[rand_mask] = arg_rand
        return arg_select

    @property
    def epsilon(self):
        return self._epsilon

    def set_epsilon(self, epsilon):
        self._epsilon = epsilon


class CategoricalEpsilonGreedy(EpsilonGreedy):
    """Input p to be shaped [T,B,A,P] or [B,A,P], A: number of actions,
    P: number of atoms.  Input z is domain of atom-values, shaped [P]."""

    def __init__(self, z=None, **kwargs):
        super().__init__(**kwargs)
        self.z = z

    def sample(self, p, z=None):
        q = torch.tensordot(p, z or self.z, dims=1)
        return super().sample(q)

    def set_z(self, z):
        self.z = z
