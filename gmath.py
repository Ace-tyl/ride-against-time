"""
gmath.py
使用 numpy 和 numba 优化游戏中所使用的数学运算
"""

from numba import njit
import numpy as np


@njit
def rad_to_deg(x):
    return x / np.pi * 180


@njit
def get_vector(x, y):
    len = np.sqrt(x * x + y * y)
    return x / len, y / len


@njit
def get_dir(x, y):
    return -np.arctan2(x, y)
