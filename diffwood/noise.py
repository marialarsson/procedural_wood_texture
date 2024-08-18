import math
import torch

from . import _diffwoodcore as m


def periodic_noise_3d(
    p: torch.Tensor,
    ) -> torch.Tensor:

    p = p.view(-1,3)
    out = torch.zeros_like(p)

    m.periodic_noise_3d(p, out)

    return out


def periodic_noise_3d_torch(
    p: torch.Tensor
    ) -> torch.Tensor:

    """Batched computation of 3D noise function

    Arguments:
        p: position tensor stacking 3D coordinates (shape = [num, 3]).

    Returns:
        noise tensor (shape = [num, 3]).
    """

    assert isinstance(p, torch.Tensor) and p.dtype == torch.float32
    p = p.view(-1,3)

    px = p[..., 0].ravel()[..., None]
    py = p[..., 1].ravel()[..., None]
    pz = p[..., 2].ravel()[..., None]

    PI = math.pi

    noiseX = torch.sin(2.0 * PI * px) * torch.cos(2.0 * PI * py) * torch.sin(2.0 * PI * pz)
    noiseX += 0.5 * torch.sin(4.0 * PI * px) * torch.cos(4.0 * PI * py) * torch.sin(4.0 * PI * pz)
    noiseX += 0.25 * torch.sin(8.0 * PI * px) * torch.cos(8.0 * PI * py) * torch.sin(8.0 * PI * pz)

    noiseY = torch.cos(2.0 * PI * px) * torch.sin(2.0 * PI * py) * torch.cos(2.0 * PI * pz)
    noiseY += 0.5 * torch.cos(4.0 * PI * px) * torch.sin(4.0 * PI * py) * torch.cos(4.0 * PI * pz)
    noiseY += 0.25 * torch.cos(8.0 * PI * px) * torch.sin(8.0 * PI * py) * torch.cos(8.0 * PI * pz)

    noiseZ = torch.sin(2.0 * PI * px + 1.0) * torch.cos(2.0 * PI * py + 1.0) * torch.sin(2.0 * PI * pz + 1.0)
    noiseZ += 0.5 * torch.sin(4.0 * PI * px + 1.0) * torch.cos(4.0 * PI * py + 1.0) * torch.sin(4.0 * PI * pz + 1.0)
    noiseZ += 0.25 * torch.sin(8.0 * PI * px + 1.0) * torch.cos(8.0 * PI * py + 1.0) * torch.sin(8.0 * PI * pz + 1.0)

    return torch.cat((noiseX, noiseY, noiseZ), dim=-1)


