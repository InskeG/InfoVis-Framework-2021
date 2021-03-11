# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Generate images using pretrained network pickle."""

from base64 import encodebytes
import io
import numpy as np
import PIL.Image
import torch


def generate_images(generator, seeds, class_idx):
    """Generate images using pretrained network pickle. """

    device = torch.device("cuda")

    # Labels.
    label = torch.zeros([1, generator.c_dim], device=device)
    label[:, class_idx] = 1

    # Generate images.
    images = []
    for seed_idx, seed in enumerate(seeds):
        z = torch.from_numpy(np.random.RandomState(seed).randn(1, generator.z_dim)).to(device)
        img = generator(z, label)
        img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
        pil_img = PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB')

        # Convert to byte array for transmission to front-end
        byte_arr = io.BytesIO()
        pil_img.save(byte_arr, format='PNG')

        images.append(encodebytes(byte_arr.getvalue()).decode('ascii'))

    return images
