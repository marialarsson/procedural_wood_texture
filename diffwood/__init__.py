from typing import Union, Tuple, List, Any
from . import cuda
from .noise import *


def gen_pix_samples(
    resolution: Tuple[int, int],
    spp_x = 1,
    device = 'cpu',
    random = False
    ) -> Tuple[torch.Tensor, torch.Tensor]:

    height, width = resolution
    spp = spp_x ** 2

    pos_x = torch.arange(width * spp_x, dtype=torch.float32, device=device)
    pos_y = torch.arange(height * spp_x, dtype=torch.float32, device=device)
    pos_x, pos_y = torch.meshgrid(pos_x, pos_y, indexing='xy')

    if random:
        pos_x = -1.0 + 2.0 * (pos_x + torch.rand_like(pos_x)) / width / spp_x
        pos_y = -1.0 + 2.0 * (pos_y + torch.rand_like(pos_y)) / height / spp_x
    else:
        pos_x = -1.0 + 2.0 * (pos_x + 0.5) / width / spp_x
        pos_y = -1.0 + 2.0 * (pos_y + 0.5) / height / spp_x

    pos_x = pos_x.view(height, spp_x, width, spp_x).permute(0, 2, 1, 3)
    pos_y = pos_y.view(height, spp_x, width, spp_x).permute(0, 2, 1, 3)
    pos_x = pos_x.contiguous().view(height, width, spp, 1)
    pos_y = pos_y.contiguous().view(height, width, spp, 1)

    return pos_x, pos_y

