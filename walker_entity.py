import pygame
import skin
import gmath
import numpy as np


class WalkerEntity:
    def __init__(self, x, y):
        self.pos_screen = np.array([x, y])
    def render(self, screen):
        nskin = skin.player_skin
        nskin = pygame.transform.rotate(nskin, gmath.rad_to_deg(self.player_dir))
        skin_rect = nskin.get_rect()
        skin_rect.center = self.pos_screen
        screen.blit(nskin, skin_rect)
