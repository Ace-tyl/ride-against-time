"""
地形生成器，实现了游戏中地形以及闲置单车的生成

地形生成：
以 640 像素（对应 12.8m）为一个区块（chunk），每个区块的地形有一个斜率值。
这个值 80% 情况下为 0，另外 20% 情况下，范围为 [-5.0, 5.0] 度，在范围内服从正态分布，标准差为 1.926。
地形会影响玩家的速度，如下坡时玩家会加速。（暂时搁置）
"""

import numpy as np
from numba import njit
from skin import bike_skin_npc


@njit
def generate_terrain_value():
    if np.random.randint(5):
        return 0
    else:
        deg = np.random.randn() * 1.926
        deg = np.minimum(deg, 5.)
        deg = np.maximum(deg, -5.)
        return deg


class terrain_generator:
    terrain = np.array([])

    def initialize_terrain(self):
        self.terrain = np.array([])

    def update_terrain(self, pos: int):
        while len(self.terrain) <= pos:
            self.terrain = np.append(self.terrain, generate_terrain_value())


class bikes_generator:
    dist = 0
    remain = 0
    prob = 0
    
    def get_next_bike(self):
        if self.remain:
            self.dist += np.random.randint(25, 35)
            self.remain -= 1
        else:
            self.dist += max(int(np.random.randn() * 666) + 1500, 50)
            self.remain = np.random.randint(2, 15)
            if np.random.randint(0, 6):
                self.prob = np.random.rand() / 5
            else:
                self.prob = np.random.rand() / 5 + 0.666
        bike_type = 0
        if np.random.rand() > self.prob:
            bike_type = np.random.randint(1, len(bike_skin_npc))
        return self.dist, bike_type
