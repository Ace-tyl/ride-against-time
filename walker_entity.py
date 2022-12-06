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

    def update_pos(self, delta_t):
        x, y = self.pos_screen
        dx, dy = self.speed_dir
        dx, dy = gmath.get_vector(dx, dy)
        sx, sy = self.speed * dx, self.speed * dy
        self.player_dir = gmath.get_dir(dx, dy)
        x += sx * delta_t
        y += sy * delta_t
        self.pos_screen = np.array([x, y])
        if np.random.rand() < delta_t / 3.14 or x < 20 or x > 480:
            if x < 20:
                self.speed_dir[0] = abs(np.random.randn())
            elif x > 480:
                self.speed_dir[0] = -abs(np.random.randn())
            else:
                self.speed_dir[0] = np.random.randn()

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
