import numba
import numpy as np


@numba.njit
def one_hot_encode(data: np.ndarray):
    data = data.transpose(1, 2, 0)
    n = data.shape[2]

    shift = np.zeros((1, 1, n), np.int32)
    shift[0, 0, :] = np.arange(0, n, 1, np.int32)
    binary = (data > 0)
    binary = (binary << shift).sum(-1)
    return binary.astype(np.int32)


@numba.njit
def one_hot_decode(data: np.ndarray, n: int):
    shift = np.zeros((1, 1, n), np.int32)
    shift[0, 0, :] = np.arange(0, n, 1, np.int32)

    x = np.zeros((*data.shape, 1), data.dtype)
    x[..., 0] = data
    x = (x >> shift) & 1
    return x.transpose(2, 0, 1)
