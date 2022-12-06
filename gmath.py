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


@njit
def get_abs(a: np.array):
    return np.sqrt(a[0] * a[0] + a[1] * a[1])


@njit
def det(a: np.array, b: np.array):
    return a[0] * b[1] - b[0] * a[1]


@njit
def rotate(a: np.array, θ):
    return np.array([a[0] * np.cos(θ) - a[1] * np.sin(θ), a[0] * np.sin(θ) + a[1] * np.cos(θ)])


class Rectangle:
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.ul = np.array([x1, y1])
        self.ur = np.array([x2, y2])
        self.dr = np.array([x3, y3])
        self.dl = np.array([x4, y4])

    def inside(self, point):
        res = det(self.ul - point, self.ur - point)
        value = det(self.ur - point, self.dr - point)
        if value * res < 0: return False
        value = det(self.dr - point, self.dl - point)
        if value * res < 0: return False
        value = det(self.dl - point, self.ul - point)
        if value * res < 0: return False
        return True

    def intersect(self, another):
        return self.inside(another.ul) or self.inside(another.ur) or self.inside(another.dr) or self.inside(another.dl)

    def rotate(self, point, degree):
        self.ul = rotate(self.ul - point, degree) + point
        self.ur = rotate(self.ur - point, degree) + point
        self.dl = rotate(self.dl - point, degree) + point
        self.dr = rotate(self.dr - point, degree) + point
        return self
