import pygame
import skin
import gmath
import numpy as np
import game


class WalkerEntity:
    def __init__(self, x, y, d):
        self.pos_screen = np.array([x, y])
        self.speed_dir = np.array([np.random.randn(), 12]) if d == 1 else np.array([np.random.randn(), -12])
        self.player_dir = gmath.get_dir(self.speed_dir[0], self.speed_dir[1])
        self.speed = 50 + np.random.rand() * 25
        self.npc_id = np.random.randint(0, skin.npc_skins_count - 1)
        self.walking_dir = d
        self.br_time = 0

    def update_pos(self, delta_t, player_data):
        x, y = self.pos_screen
        dx, dy = self.speed_dir
        dx, dy = gmath.get_vector(dx, dy)
        sx, sy = self.speed * dx, self.speed * dy
        self.player_dir = gmath.get_dir(dx, dy)
        x += sx * delta_t
        y += sy * delta_t
        self.pos_screen = np.array([x, y])
        v⃗ = self.get_speed_vector()
        v⃗_player = player_data.get_speed_vector()
        v⃗_relative = v⃗ - v⃗_player
        r⃗ = self.pos_screen
        r⃗_player = player_data.pos_screen.copy()
        r⃗_player[1] = 600 - r⃗_player[1] + game.s_dist
        r⃗_relative = r⃗_player - r⃗
        self.br_time += delta_t
        if self.br_time > 180 / (player_data.get_accurate_speed() + 50) and (np.dot(r⃗_relative, v⃗_relative) / gmath.get_abs(r⃗_relative) / gmath.get_abs(v⃗_relative) < 0.9
                or (gmath.get_abs(r⃗_relative) - 60) / gmath.get_abs(v⃗_relative) > 0.5):  # 在安全距离
            if np.random.rand() < delta_t / 3.14 or abs(self.speed_dir[0]) > 6:
                self.speed_dir[0] = np.random.randn()
        if x < 20 or x > 480:
            if x < 20:
                self.speed_dir[0] = abs(np.random.randn())
            else:
                self.speed_dir[0] = -abs(np.random.randn())
        if np.dot(r⃗_relative, v⃗) / gmath.get_abs(r⃗_relative) / gmath.get_abs(v⃗) > 0.95 \
                and np.dot(r⃗_relative, v⃗_relative) / gmath.get_abs(r⃗_relative) / gmath.get_abs(v⃗_relative) > 0.95 \
                and (gmath.get_abs(r⃗_relative) - 60) / gmath.get_abs(v⃗_relative) < np.abs(np.random.randn()) * 0.5:  # 不在安全距离，进行避让
            sin_th = gmath.det(r⃗_relative, v⃗_relative) / gmath.get_abs(r⃗_relative) / gmath.get_abs(v⃗_relative)
            if abs(sin_th) > 0.05:
                br_dir = 1 if sin_th > 0 else -1
            else:
                br_dir = -1 if r⃗[0] * np.random.rand() - (500 - r⃗[0]) * np.random.rand() > 0 else 1
            self.speed_dir[0] = br_dir * (12 + np.random.randn() * 6)
            self.br_time = 0

    def get_speed_vector(self):
        return gmath.rotate(np.array([0, self.speed]), self.player_dir)

    def render(self, screen):
        nskin = skin.npc_skins[self.npc_id]
        nskin = pygame.transform.rotate(nskin, gmath.rad_to_deg(self.player_dir))
        skin_rect = nskin.get_rect()
        skin_rect.center = [self.pos_screen[0], 600 - self.pos_screen[1] + game.s_dist]
        screen.blit(nskin, skin_rect)

    def get_rectangle(self):
        x, y = self.pos_screen
        return gmath.Rectangle(x - 12, y - 12, x + 12, y - 12, x + 12, y + 12, x - 12, y + 12).rotate(np.array([x, y]), self.player_dir)
