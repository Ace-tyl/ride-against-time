import pygame
import player
import time
import os
import sys
import gmath
import terrain
import bike_entity
import configfile
import walker_entity
from button import Button

mode = 0  # 0 表示限时，1 表示定距
mode_str = ""
lim = -1
s_dist = 0  # 距离
s_time = 0  # 时间
rec_str = ""


def meta_data_display(screen, font, me, fps):
    lines = []
    lines.append("{} FPS".format("Unknown" if fps == -1 else "{:.03f}".format(fps)))
    lines.append("当前距离：{:.02f}m".format(s_dist / 50))
    lines.append("时间：{}:{:02d}.{:03d}".format(s_time // 60000, s_time % 60000 // 1000, s_time % 1000))
    lines.append("玩家生命值：{:.02f}/10.00".format(me.health))
    my_speed = me.get_accurate_speed()
    lines.append("玩家速度：{:.02f}m/s{}".format(my_speed / 50, "" if my_speed < 1e-3 else "（方向 {:03d}）".format(int(-gmath.rad_to_deg(me.player_dir) + 90) % 360)))
    if me.mode == 1:
        lines.append("单车最大速度：{:.02f}m/s".format(me.bike_speed / 50))
        lines.append("刹车属性：{:.02f} // {:.02f}".format(me.ls, me.rs))

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

    endline_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Endline.png")), (500, 50))

    s_time = 0
    s_dist = 0

    pygame.display.set_caption(f"西操赶五教 — {mode_str}")
    mx, my = pygame.mouse.get_pos()
    me = player.Player()
    bikes_l, bikes_r = [], []
    walkers = []
    riders = []
    start_time = time.time()
    last_time = time.time()
    # tg = terrain.terrain_generator()
    frame_time = []
    bike_gen_l = terrain.bikes_generator()
    bike_gen_r = terrain.bikes_generator()
    npc_gen = terrain.npc_generator()

    is_key_left = False
    is_key_right = False
    is_key_return = False
    is_sc_left = False
    is_sc_right = False
    key_return_time = 0
    object_bike = None

    while True:
        current_time = time.time()
        s_time = int((current_time - start_time) * 1000)

        # Display data & entities
        # The player must be rendered at last
        screen.blit(background_img, (0, s_dist % 800))
        screen.blit(background_img, (0, s_dist % 800 - 800))
        if mode == 1: screen.blit(endline_image, (0, 575 - (lim - s_dist)))
        for entity in bikes_l + bikes_r: entity.render(screen, s_dist)
        for entity in walkers + riders: entity.render(screen)
        me.render(screen)
        time_interval = current_time - last_time

        frame_time.append(current_time)
        if len(frame_time) > 100:
            frame_time = frame_time[1:]
        meta_data_display(screen, font, me, -1 if len(frame_time) < 100 else 100 / (frame_time[-1] - frame_time[0]))
        pygame.display.flip()
        me.update_pos(time_interval)
        # tg.update_terrain(int(s_dist // 640) + 4)

        # Process player events
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
                    # else:
                    #     me.player_dir = 0.0
                    #     me.speed_dir = (0, 1)
                elif event.key == pygame.K_LEFT:
                    if me.mode == 0: me.speed_dir[0] -= 1.0
                    else: is_key_left = True
                elif event.key == pygame.K_RIGHT:
                    if me.mode == 0: me.speed_dir[0] += 1.0
                    else: is_key_right = True
                elif event.key == pygame.K_DOWN:
                    if me.mode == 0: me.speed_dir[1] -= 1.0
                elif event.key == pygame.K_RETURN:
                    if me.mode == 0:
                        object_bike = None
                        for bike in bikes_l:
                            if bike.t == 0 and bike.test_collide(me.pos_screen[0], me.pos_screen[1]):
                                object_bike = (0, bike)
                                break
                        if object_bike is None:
                            for bike in bikes_r:
                                if bike.t == 0 and bike.test_collide(me.pos_screen[0], me.pos_screen[1]):
                                    object_bike = (1, bike)
                                    break
                        if object_bike is not None:
                            is_key_return = True
                            key_return_time = current_time
                    else:
                        if me.speed > 60:
                            continue
                        try:
                            bike = me.dispose_bike()
                            if bike.lr == 0:
                                for i in range(len(bikes_l)):
                                    if bikes_l[i].pos > bike.pos:
                                        bikes_l.insert(i, bike)
                                        break
                            else:
                                for i in range(len(bikes_r)):
                                    if bikes_r[i].pos > bike.pos:
                                        bikes_r.insert(i, bike)
                                        break
                        except Exception as e:
                            pass
                elif event.key == pygame.K_SPACE:
                    if me.mode == 1: me.accelerate()
                elif event.key == pygame.K_z:
                    if me.mode == 1: is_sc_left = True
                elif event.key == pygame.K_x:
                    if me.mode == 1: is_sc_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if me.mode == 0: me.speed_dir[1] -= 1.0
                elif event.key == pygame.K_LEFT:
                    if me.mode == 0: me.speed_dir[0] += 1.0
                    else: is_key_left = False
                elif event.key == pygame.K_RIGHT:
                    if me.mode == 0: me.speed_dir[0] -= 1.0
                    else: is_key_right = False
                elif event.key == pygame.K_DOWN:
                    if me.mode == 0: me.speed_dir[1] += 1.0
                elif event.key == pygame.K_RETURN:
                    is_key_return = False
                    key_return_time = 0
                elif event.key == pygame.K_z:
                    is_sc_left = False
                elif event.key == pygame.K_x:
                    is_sc_right = False

        # Try get bike
        if is_key_return and object_bike[1].open_t < 10 and object_bike[1].open_t < current_time - key_return_time:
            is_key_return = False
            key_return_time = 0
            me.get_bike(object_bike[1])
            (bikes_r if object_bike[0] else bikes_l).remove(object_bike[1])

        # Move player
        if is_key_left:
            me.player_dir += time_interval
            me.speed_dir = gmath.get_dir_vector(me.player_dir)
        if is_key_right:
            me.player_dir -= time_interval
            me.speed_dir = gmath.get_dir_vector(me.player_dir)
        if me.mode == 1:
            me.update_speed(time_interval)
            me.decelerate(is_sc_left, is_sc_right, time_interval)

        # Generate bike
        while not len(bikes_l) or bikes_l[-1].pos < s_dist + 1145:
            npos, t = bike_gen_l.get_next_bike()
            bikes_l.append(bike_entity.bike(npos, t, 0))
        while not len(bikes_r) or bikes_r[-1].pos < s_dist + 1145:
            npos, t = bike_gen_r.get_next_bike()
            bikes_r.append(bike_entity.bike(npos, t, 1))

        # Dispose old bike
        while len(bikes_l) and bikes_l[0].pos < s_dist - 314:
            bikes_l = bikes_l[1:]
        while len(bikes_r) and bikes_r[0].pos < s_dist - 314:
            bikes_r = bikes_r[1:]

        # Generate Walker NPC
        gen_npc = npc_gen.generate_npcs(s_dist, time_interval)
        if gen_npc is not None:
            npc = walker_entity.WalkerEntity(gen_npc[0][0], gen_npc[0][1], gen_npc[1])
            walkers.append(npc)

        # Walker Move
        for walker in walkers:
            walker.update_pos(time_interval, me)

        # Dispose Walker NPC
        for walker in walkers:
            if walker.pos_screen[1] < s_dist - 600 or walker.pos_screen[1] > s_dist + 1200:
                walkers.remove(walker)

        # Test collision
        player_rect = me.get_rectangle()
        for entity in bikes_l + bikes_r + walkers + riders:
            rect = entity.get_rectangle()
            if player_rect.intersect(rect):
                relative_speed_vector = me.get_speed_vector() - entity.get_speed_vector()
                relative_speed = gmath.get_abs(relative_speed_vector)
                if me.get_accurate_speed() == 0: continue
                if me.mode == 1:
                    if me.speed > 60: me.get_damage(relative_speed**2 / 10000, 19268)
                    else: me.get_damage((relative_speed - 70) / 200, 11451)
                else:
                    me.get_damage((relative_speed - 70) / 60 * time_interval, 11451)

        # Judge player death
        if me.health < 0:
            main.game_mode = -me.health
            return

        # Judge game over
        if mode == 0 and s_time > lim or mode == 1 and s_dist > lim:
            main.game_mode = 1926
            return

        last_time = current_time


def game_over(screen, font, font_large):
    from gameselector import background_img
    import main

    def go_back():
        main.game_mode = 1

    screen.fill((0, 0, 0))
    bg_image = background_img
    bg_image.set_alpha(192)
    screen.blit(bg_image, (0, s_dist % 800))
    screen.blit(bg_image, (0, s_dist % 800 - 800))

    text = font_large.render("你寄了" if main.game_mode > 10000 else ("时间到" if mode == 0 else "到达终点"), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (250, 144)
    screen.blit(text, textRect)

    if main.game_mode > 10000:
        if main.game_mode == 10492:
            text_str = "你太嗨了，冲出了道路"
        elif main.game_mode == 10388:
            text_str = "你甚至没有意识到这是一个卷轴游戏"
        elif main.game_mode == 19268:
            text_str = "行车不规范，亲人两行泪"
        elif main.game_mode == 11451:
            text_str = "迎面走来的你，让我如此蠢蠢欲动"
        text = font.render(text_str, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (250, 216)
        screen.blit(text, textRect)

    button_back = Button(125, 450, "返回主页面", go_back)
    buttons = [button_back]

    if mode == 0:
        result = configfile.get_config(rec_str, -1)
        text = font.render("{}：{:.02f}m".format("新纪录" if s_dist > result else "距离", s_dist / 50), True, (255, 128, 128) if s_dist > result else (255, 255, 255))
        if s_dist > result:
            configfile.change_config(rec_str, s_dist)
            configfile.write_config()
        textRect = text.get_rect()
        textRect.center = (250, 256)
        screen.blit(text, textRect)

    if mode == 1:
        if main.game_mode <= 10000:
            result = configfile.get_config(rec_str, -1)
            if result == -1: result = 1e145
            text = font.render("{}：{}:{:02d}.{:03d}".format("新纪录" if s_time < result else "用时", s_time // 60000, s_time % 60000 // 1000, s_time % 1000), True, (255, 128, 128) if s_time < result else (255, 255, 255))
            if s_time < result:
                configfile.change_config(rec_str, s_time)
                configfile.write_config()
            textRect = text.get_rect()
            textRect.center = (250, 256)
            screen.blit(text, textRect)

    pygame.display.flip()

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
        if main.game_mode < 1000:
            return
