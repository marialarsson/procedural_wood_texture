import torch

from . import _diffwoodcore as m


def periodic_noise_3d(
    p: torch.Tensor,
    ) -> torch.Tensor:

    p = p.view(-1,3)
    out = torch.zeros_like(p)

    m.periodic_noise_3d(p, out)

    return out
