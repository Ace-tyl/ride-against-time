import pygame
import os

player_skin = pygame.image.load(os.path.join("skins", "player.png"))
player_skin = pygame.transform.scale(player_skin, (32, 32))