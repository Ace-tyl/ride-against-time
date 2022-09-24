import pygame
import configfile

if __name__ == '__main__':
    pygame.init()

import os
from button import Button

background_img = pygame.image.load(os.path.join("assets", "AboutPage.jpg"))

passage = open(os.path.join("assets", "readme.txt"), "r").read()


def splitLines(text):
    lines = text.split('\n')
    line_width = 42
    tmpstr = ""
    tmpstrlen = 0
    word = ""
    result = []

    for line in lines:
        line += ' '
        for ch in line:
            if ord(ch) > 256:  # 是一个中文字符，占用两格，一字为一词
                if tmpstrlen + len(word) <= line_width:
                    tmpstr += word
                    tmpstrlen += len(word)
                else:
                    result.append(tmpstr)
                    tmpstr = word
                    tmpstrlen = len(word)
                word = ''
                if tmpstrlen <= line_width - 2:
                    tmpstr += ch
                    tmpstrlen += 2
                else:
                    result.append(tmpstr)
                    tmpstr = ch
                    tmpstrlen = 2
            elif ch == ' ':  # 是一个空格
                if tmpstrlen + len(word) <= line_width:
                    tmpstr += word
                    tmpstrlen += len(word)
                else:
                    result.append(tmpstr)
                    tmpstr = word
                    tmpstrlen = len(word)
                word = ''
                tmpstr += ' '
            else:
                word += ch
        result.append(tmpstr)
        tmpstr = ""
        tmpstrlen = 0

    return result


def splitPages(lines):
    result = []
    linesPerPage = 23
    for i in range(0, len(lines), linesPerPage):
        result.append(lines[i: i + linesPerPage])
    return result


passage = splitLines(passage)
passage = splitPages(passage)


def refresh_page(page, splitted_text, screen, font):
    screen.fill((255, 255, 255))
    screen.blit(background_img, (0, 0))
    content = splitted_text[page]
    curX = 60
    for line in content:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (100, curX))
        curX += 26
    text = font.render(f"第 {page + 1} 页，共 {len(passage)} 页", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (260, 680)
    screen.blit(text, textRect)


def execute(screen, font):
    import main

    def go_back():
        main.game_mode = 1

    configfile.change_config("aboutRead", 1)
    refresh_page(0, passage, screen, font)
    pygame.display.set_caption("西操赶五教 — 游戏说明")

    button_back = Button(125, 735, "返回主页面", go_back)
    buttons = [button_back]

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
                if event.key == pygame.K_LEFT and page:
                    page -= 1
                    refresh_page(page, passage, screen, font)
                if event.key == pygame.K_RIGHT and page != len(passage) - 1:
                    page += 1
                    refresh_page(page, passage, screen, font)

        pygame.time.delay(16)
        for button in buttons:
            button.draw(screen)  # 更新按钮状态
        pygame.display.flip()
        if main.game_mode != 12:
            return


if __name__ == '__main__':
    print(passage)
