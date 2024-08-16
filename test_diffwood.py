import torch

import diffwood as dw


if __name__ == '__main__':
    print('cuda.is_available() =', dw.cuda.is_available())


    height, width = 128, 128
    x,y = dw.gen_pix_samples((height, width))

    x = x.view(-1,1)
    y = y.view(-1,1)
    p = torch.cat((x, y, 0.5*torch.ones_like(x)), dim=1)

    noise = dw.periodic_noise_3d(p).view(height, width, 3)
    noise = noise.detach().cpu().numpy()



    import os
    import matplotlib.pyplot as plt

    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)

    plt.clf()
    plt.title('NoiseX')
    plt.imshow(noise[..., 0])
    plt.savefig(os.path.join(output_dir, './noise.png'))



    if dw.cuda.is_available() and torch.cuda.is_available():
        p = p.cuda()
        noise = dw.periodic_noise_3d(p).view(height, width, 3)
        noise = noise.detach().cpu().numpy()

        plt.clf()
        plt.title('NoiseX')
        plt.imshow(noise[..., 0])
        plt.savefig(os.path.join(output_dir, './noise_cuda.png'))


