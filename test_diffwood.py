import torch

import diffwood as dw


if __name__ == '__main__':
    print('cuda.is_available() =', dw.cuda.is_available())


    p = 0.5 * torch.ones(100,3)
    noise = dw.periodic_noise_3d(p)

    print(noise)

