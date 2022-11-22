import pygame
import skin
import game
import numpy as np
import gmath
from bike_entity import bike


class Player:
    mode = 0  # 0 表示玩家在走路状态，1 表示骑车状态
    health = 10.0
    pos_screen = np.array([250.0, 600.0])
    speed = 60.0
    speed_dir = np.array([0.0, 0.0])
    player_dir = 0.0
    being_damaged = 0
    # Below is bike properties
    bike_speed = 0
    ls, rs = 0, 0
    bike_ot = 0

    def get_damage(self, value):
        if value <= 0: return
        self.being_damaged = 10
        self.health -= value
        if self.mode == 1: self.speed = 0.0

    def update_pos(self, delta_t):
        if not self.speed_dir[0] and not self.speed_dir[1]: return
        x, y = self.pos_screen
        dx, dy = self.speed_dir
        dx, dy = gmath.get_vector(dx, dy)
        sx, sy = self.speed * dx, self.speed * dy
        self.player_dir = gmath.get_dir(dx, dy)
        x += sx * delta_t
        y -= sy * delta_t
        x = max(x, 16)
        x = min(x, 484)
        y = min(y, 784)
        if x <= 16: self.get_damage(-sx / (4000 if not self.mode else 40))  # 尝试越界，扣血
        if x >= 484: self.get_damage(sx / (4000 if not self.mode else 40))
        if y >= 784: self.get_damage(-sy / (4000 if not self.mode else 40))
        if y < 600:
            game.s_dist += 600 - y
            y = 600
        self.pos_screen = np.array([x, y])

    def render(self, screen):
        if self.mode == 1:
            nbike = skin.bike_skin
            nbike = pygame.transform.rotate(nbike, gmath.rad_to_deg(self.player_dir))
            bike_rect = nbike.get_rect()
            bike_rect.center = self.pos_screen
            screen.blit(nbike, bike_rect)
        self.being_damaged -= 1
        nskin = skin.player_skin
        nskin = pygame.transform.rotate(nskin, gmath.rad_to_deg(self.player_dir))
        nskin.set_alpha(255 - self.being_damaged * 10)
        skin_rect = nskin.get_rect()
        skin_rect.center = self.pos_screen
        screen.blit(nskin, skin_rect)

    def get_bike(self, bike):
        self.mode = 1
        self.speed = 0
        self.speed_dir = (1.0 if bike.lr == 0 else -1.0, 0.0)
        self.bike_speed = bike.speed
        self.ls, self.rs = bike.ls, bike.rs
        self.bike_ot = bike.open_t

    def dispose_bike(self):
        returned_pos = -1
        if self.pos_screen[0] < 60:
            returned_pos = 0
        elif self.pos_screen[0] > 440:
            returned_pos = 1
        if returned_pos == -1:
            raise Exception("嗯哼哼，啊啊啊啊啊啊啊啊啊！")
        self.mode = 0
        self.speed = 60.0
        self.speed_dir = np.array([0.0, 0.0])
        return bike(600 - self.pos_screen[1] + game.s_dist, 0, returned_pos, self.bike_speed, self.ls, self.rs, self.bike_ot)

    def get_accurate_speed(self):
        if not self.speed_dir[0] and not self.speed_dir[1]: return 0
        else: return self.speed

    def update_speed(self, time_interval):
        self.speed -= time_interval * gmath.μ * gmath.g  # f = μmg; f = μmg cos θ - mg sin θ
        if self.speed < 0: self.speed = 0.0

    def accelerate(self):
        if self.speed > self.bike_speed: return
        self.speed += (self.bike_speed - self.speed) / 10

    def decelerate(self, is_l, is_r, time_interval):
        if is_l: self.speed -= time_interval * self.ls * gmath.g
        if is_r: self.speed -= time_interval * self.rs * gmath.g
        if self.speed < 0: self.speed = 0.0
