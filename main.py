import pygame
import sys

pygame.init()
font = pygame.font.Font("fonts/unifont-13.0.06.ttf", 16)

screen = pygame.display.set_mode((600, 400))
screen.fill((255, 255, 255))
pygame.display.set_caption("西操赶五教")

text = font.render("开始游戏 Start Game 114514", True, (0, 0, 0), (255, 255, 255))
textRect = text.get_rect()
textRect.center = (300, 200)
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()