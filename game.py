import pygame
import player
import time
import sys
import gmath
import terrain
import bike_entity

mode = 0  # 0 表示限时，1 表示定距
mode_str = ""
lim = -1
s_dist = 0  # 距离
s_time = 0  # 时间


def meta_data_display(screen, font, me, fps):
    lines = []
    lines.append("{} FPS".format("Unknown" if fps == -1 else "{:.03f}".format(fps)))
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
    tg = terrain.terrain_generator()
    frame_time = []
    bike_gen_l = terrain.bikes_generator()
    bike_gen_r = terrain.bikes_generator()

    is_key_left = False
    is_key_right = False
    is_key_return = False
    key_return_time = 0
    object_bike = None

    def time_out():
        pass

    while True:
        current_time = time.time()
        s_time = int((current_time - start_time) * 1000)
        if mode == 0 and s_time >= lim:
            time_out()

        # Display data & entities
        # The player must be rendered at last
        screen.blit(background_img, (0, s_dist % 800))
        screen.blit(background_img, (0, s_dist % 800 - 800))
        for entity in walkers: entity.render(screen)
        for entity in riders: entity.render(screen)
        for entity in bikes_l: entity.render(screen, s_dist)
        for entity in bikes_r: entity.render(screen, s_dist)
        me.render(screen)
        time_interval = current_time - last_time

        frame_time.append(current_time)
        if len(frame_time) > 100:
            frame_time = frame_time[1:]
        meta_data_display(screen, font, me, -1 if len(frame_time) < 100 else 100 / (frame_time[-1] - frame_time[0]))
        pygame.display.flip()
        me.update_pos(time_interval)
        tg.update_terrain(int(s_dist // 640) + 4)

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
                    else:
                        me.player_dir = 0.0
                        me.speed_dir = (0, 1)
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
                        try:
                            bike = me.dispose_bike()
                            if bike.lr == 0:
                                for i in range(len(bikes_l)):
                                    if bikes_l[i].pos > bike.pos:
                                        bikes_l.insert(i, bike)
                                        break
                            else:
                                for i in range(len(bikes_r)):
                                    print(bikes_r[i].pos)
                                    if bikes_r[i].pos > bike.pos:
                                        bikes_r.insert(i, bike)
                                        print(1145141919810)
                                        break
                        except Exception as e:
                            pass
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

        last_time = current_time
