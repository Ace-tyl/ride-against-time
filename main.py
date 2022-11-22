import pygame
import os
import sys
import configfile

pygame.init()
configfile.read_config()
screen = pygame.display.set_mode((500, 800))

import font
import skin
import titlepage
import aboutpage
import gameselector
import game

iconfile = pygame.image.load(os.path.join("assets", "Icon.png"))
iconfile.blit(skin.player_skin, (20, 10))
pygame.display.set_icon(iconfile)

game_mode = 1

while True:
    if game_mode == 0:
        exit(0)
    elif game_mode == 1:
        titlepage.execute(screen, font.font)
    elif game_mode == 12:
        aboutpage.execute(screen, font.font)
    elif game_mode == 11:
        gameselector.execute(screen, font.font)
    elif game_mode == 114:
        game.run_game(screen, font.font)
    elif game_mode > 1000:
        game.game_over(screen, font.font, font.font_large)
