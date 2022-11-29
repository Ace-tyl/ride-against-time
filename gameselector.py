import pygame
import sys
import configfile
import game

import os
from button import Button

background_img = pygame.image.load(os.path.join("assets", "GameBackground.jpg"))

passage = open(os.path.join("assets", "readme.txt"), "r").read()


def get_record(s: str, mode):
    result = configfile.get_config(s, -1)
    if result == -1: return ""
    if mode == 0: return " (纪录 {:.02f}m)".format(result / 50)
    else: return " (纪录 {}:{:02d}.{:03d})".format(result // 60000, result % 60000 // 1000, result % 1000)


def execute(screen, font):
    import main

    def go_back():
        main.game_mode = 1

    def engame(ms, rs, lm):
        main.game_mode = 114
        game.mode = 0
        game.lim = lm
        game.mode_str = ms
        game.rec_str = rs

    def dsgame(ms, rs, lm):
        main.game_mode = 114
        game.mode = 1
        game.lim = lm
        game.mode_str = ms
        game.rec_str = rs

    screen.fill((255, 255, 255))
    pygame.display.set_caption("西操赶五教 — 选择模式")
    screen.blit(background_img, (0, 0))

    text = font.render("选择游戏模式", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (250, 80)
    screen.blit(text, textRect)

    button_back = Button(125, 735, "返回主页面", go_back)
    button_gamemode_tl_5 = Button(125, 110, f"限时 5min{get_record('rec5min', 0)}", lambda: engame("限时 5min", "rec5min", 300000))
    button_gamemode_tl_10 = Button(125, 170, f"限时 10min{get_record('rec10min', 0)}", lambda: engame("限时 10min", "rec10min", 600000))
    button_gamemode_tl_15 = Button(125, 230, f"限时 15min{get_record('rec15min', 0)}", lambda: engame("限时 15min", "rec15min", 900000))
    button_gamemode_tl_20 = Button(125, 290, f"限时 20min{get_record('rec20min', 0)}", lambda: engame("限时 20min", "rec20min", 1200000))
    button_gamemode_ds_1 = Button(125, 350, f"定距 1km{get_record('rec1km', 1)}", lambda: dsgame("定距 1km", "rec1km", 50000))
    button_gamemode_ds_2 = Button(125, 410, f"定距 2km{get_record('rec2km', 1)}", lambda: dsgame("定距 2km", "rec2km", 100000))
    button_gamemode_ds_3 = Button(125, 470, f"定距 3km{get_record('rec3km', 1)}", lambda: dsgame("定距 3km", "rec3km", 150000))
    button_gamemode_ds_5 = Button(125, 530, f"定距 5km{get_record('rec5km', 1)}", lambda: dsgame("定距 5km", "rec5km", 250000))
    buttons = [button_back, button_gamemode_tl_5, button_gamemode_tl_10, button_gamemode_tl_15, button_gamemode_tl_20, button_gamemode_ds_1, button_gamemode_ds_2, button_gamemode_ds_3, button_gamemode_ds_5]

    page = 0

    while True:
        mx, my = pygame.mouse.get_pos()  # 获取鼠标的位置

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.getFocus(mx, my)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    for button in buttons:
                        button.mouseDown(mx, my)
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    button.mouseUp()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    go_back()

        pygame.time.delay(16)
        for button in buttons:
            button.draw(screen)  # 更新按钮状态
        pygame.display.flip()
        if main.game_mode != 11:
            return
