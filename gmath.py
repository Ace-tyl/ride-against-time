"""
gmath.py
使用 numpy 和 numba 优化游戏中所使用的数学运算
"""

import numpy as np
from numba import njit


μ = np.float64(.25)
g = np.float64(49)


@njit
def rad_to_deg(x):
    return x / np.pi * 180


@njit
def deg_to_rad(x):
    return x / 180 * np.pi


@njit
def get_vector(x, y):
    len = np.sqrt(x * x + y * y)
    return x / len, y / len


@njit
def get_dir(x, y):
    return -np.arctan2(x, y)


@njit
def get_dir_vector(dir):
    return np.array([np.sin(-dir), np.cos(-dir)])
