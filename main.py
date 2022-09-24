import pygame
import sys
import configfile

pygame.init()
configfile.read_config()

import font
import titlepage, aboutpage

screen = pygame.display.set_mode((500, 800))

game_mode = 1

while True:
    if game_mode == 0:
        exit(0)
    elif game_mode == 1:
        titlepage.execute(screen, font.font)
    elif game_mode == 12:
        aboutpage.execute(screen, font.font)
