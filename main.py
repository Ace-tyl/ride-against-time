import pygame
import sys

pygame.init()

import font
import titlepage

screen = pygame.display.set_mode((500, 800))

game_mode = 1

while True:
    if game_mode == 0:
        exit(0)
    elif game_mode == 1:
        titlepage.execute(screen, font.font)