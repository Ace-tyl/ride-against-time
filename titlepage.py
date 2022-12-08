import pygame
import os
import sys
import skin
from button import Button
import configfile

background_img = pygame.image.load(os.path.join("assets", "TitlePage.jpg"))


def execute(screen, font):
    import main

    def exit_game():
        main.game_mode = 0

    def enter_about():
        main.game_mode = 12

    def start_game():
        main.game_mode = 11

    screen.fill((255, 255, 255))
    screen.blit(background_img, (0, 0))
    pygame.display.set_caption("西操赶五教")

    screen.blit(skin.player_skin, (151, 735))

    button_start_game = Button(125, 300, "开始游戏", start_game)
    button_about = Button(125, 375, f"游戏说明{'' if configfile.get_config('aboutRead') else ' (请仔细阅读)'}", enter_about)
    button_exit = Button(125, 450, "退出游戏", exit_game)
    buttons = [button_start_game, button_about, button_exit]

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
                    pygame.quit()
                    sys.exit()

        pygame.time.delay(50)
        for button in buttons:
            button.draw(screen)  # 更新按钮状态
        pygame.display.flip()
        if main.game_mode != 1:
            return
