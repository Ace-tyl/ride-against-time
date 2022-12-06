import numpy as np
import pygame
import skin
import game
import gmath


class bike:
    pos = 0
    x = 0
    t = 0
    lr = 0
    # Below is bike properties
    speed = 0
    ls, rs = 0, 0
    open_t = 0

    def __init__(self, pos, t, lr, speed=-1, ls=-1, rs=-1, ot=-1):
        self.pos = pos
        self.x = 460 if lr else 40
        self.t = t
        self.lr = lr
        if speed != -1:
            self.speed = speed
            self.ls = ls
            self.rs = rs
            self.open_t = ot
            return
        self.speed = np.random.rand() * 120 + 180
        if np.random.randint(0, 20):
            self.ls = np.random.rand() * .2 + 1.2
        if np.random.randint(0, 20):
            self.rs = np.random.rand() * .2 + 1.2
        self.open_t = np.random.randn() * 4 + 4
        self.open_t = max(self.open_t, 3.0)

    def test_collide(self, x, y):
        nx, ny = self.x, self.pos
        if x < nx - 40 or x > nx + 40:
            return False
        if 600 - y + game.s_dist < ny - 20 or 600 - y + game.s_dist > ny + 20:
            return False
        return True

    def render(self, screen, init_pos):
        nbike = skin.bike_skin
        if self.t:
            nbike = skin.bike_skin_npc[self.t - 1]
        nx, ny = self.x, 600 - self.pos + init_pos
        if self.lr: nbike = pygame.transform.rotate(nbike, -90)
        else: nbike = pygame.transform.rotate(nbike, 90)
        bike_rect = nbike.get_rect()
        bike_rect.center = (nx, ny)
        screen.blit(nbike, bike_rect)

    def get_speed_vector(self):
        return np.array([0, 0])

    def get_rectangle(self):
        x, y = self.x, self.pos
        return gmath.Rectangle(x - 30, y - 12, x + 30, y - 12, x + 30, y + 12, x - 30, y + 12)
