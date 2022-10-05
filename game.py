import pygame
import player
import time
import sys
import gmath

mode = 0  # 0 表示限时，1 表示定距
mode_str = ""
lim = -1
s_dist = 0  # 距离
s_time = 0  # 时间


def meta_data_display(screen, font, me):
    lines = []
    lines.append("当前距离：{:.02f}m".format(s_dist / 50))
    lines.append("时间：{}:{:02d}.{:03d}".format(s_time // 60000, s_time % 60000 // 1000, s_time % 1000))
    lines.append("玩家生命值：{:.02f}/10.00".format(me.health))
    my_speed = me.get_accurate_speed()
    lines.append("玩家速度：{:.02f}m/s{}".format(my_speed / 50, "" if my_speed < 1e-3 else "（方向 {:03d}）".format(int(-gmath.rad_to_deg(me.player_dir) + 90) % 360)))

    cur_y = 5
    red = me.health <= 3.14159
    for line in lines:
        text = font.render(line, True, (255 if red else 0, 0 if red else 255, 0))
        screen.blit(text, (93, cur_y))
        cur_y += 25


def run_game(screen, font):
    global s_time, s_dist
    import main
    from gameselector import background_img

    pygame.display.set_caption(f"西操赶五教 — {mode_str}")
    mx, my = pygame.mouse.get_pos()
    me = player.Player()
    bikes = []
    walkers = []
    riders = []
    start_time = time.time()
    last_time = time.time()

    def time_out():
        pass

    while True:
        current_time = time.time()
        s_time = int((current_time - start_time) * 1000)
        if mode == 0 and s_time >= lim:
            time_out()
        screen.blit(background_img, (0, s_dist % 800))
        screen.blit(background_img, (0, s_dist % 800 - 800))
        me.render(screen)
        for entity in bikes: entity.render(screen)
        for entity in walkers: entity.render(screen)
        for entity in riders: entity.render(screen)
        meta_data_display(screen, font, me)
        pygame.display.flip()
        me.update_pos(current_time - last_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main.game_mode = 11
                    return
                elif event.key == pygame.K_UP:
                    if me.mode == 0: me.speed_dir[1] += 1.0
                elif event.key == pygame.K_LEFT:
                    if me.mode == 0: me.speed_dir[0] -= 1.0
                elif event.key == pygame.K_RIGHT:
                    if me.mode == 0: me.speed_dir[0] += 1.0
                elif event.key == pygame.K_DOWN:
                    if me.mode == 0: me.speed_dir[1] -= 1.0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if me.mode == 0: me.speed_dir[1] -= 1.0
                elif event.key == pygame.K_LEFT:
                    if me.mode == 0: me.speed_dir[0] += 1.0
                elif event.key == pygame.K_RIGHT:
                    if me.mode == 0: me.speed_dir[0] -= 1.0
                elif event.key == pygame.K_DOWN:
                    if me.mode == 0: me.speed_dir[1] += 1.0

        last_time = current_time
        pygame.time.delay(16)
