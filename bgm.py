import pygame
import os

pygame.mixer.init()
pygame.mixer.music.load(os.path.join("assets", "game_bgm.ogg"))


def start_bgm():
    pygame.mixer.music.play(-1)


def end_bgm():
    pygame.mixer.music.stop()
