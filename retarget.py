import numpy as np


def patches(matrix):
    patch_size = 4
    patches = []
    for i in range(matrix.shape[0] - patch_size):
        for j in range(matrix.shape[1] - patch_size):
            patch = matrix[i:i + patch_size, j:j + patch_size]
            patches.append(patch)
    return patches


def retarget(source, target):
    pass


im = np.array([
    [0, 1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1, 0],
])

ps = patches(im)
print(patches(im))
import pdb
pdb.set_trace()
