import numpy as np


def build_default_kernel(kernel_width, separable=False, normalize=False):
    base_kernel = [2 ** x for x in range(kernel_width // 2)]
    kernel = base_kernel + [2 ** (kernel_width // 2)] + base_kernel[::-1]
    kernel = np.array(kernel)[..., None]

    if not separable:
        kernel = np.matmul(kernel, kernel.T)

    if normalize:
        kernel = kernel / sum(kernel.flatten())

    return kernel.astype(np.float32)
