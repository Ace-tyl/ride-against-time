import pygame
import os

player_skin = pygame.image.load(os.path.join("skins", "player.png"))
player_skin = pygame.transform.scale(player_skin, (25, 25)).convert_alpha()

bike_skin = pygame.image.load(os.path.join("assets", "bike.png")).convert_alpha()
bike_skin_npc_template = pygame.image.load(os.path.join("assets", "bike_template.png")).convert_alpha()

bike_skin_npc = []

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 255), (11, 45, 14)]
filling_rect = pygame.Rect((11, 1), (4, 59))

for color in colors:
    surface = pygame.Surface((25, 60), flags=pygame.SRCALPHA)
    surface = surface.convert_alpha()
    surface.fill(color, filling_rect)
    surface.blit(bike_skin_npc_template, (0, 0))
    bike_skin_npc.append(surface)
