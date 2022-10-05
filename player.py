import pygame
import skin
import game
import gmath


class Player:
    mode = 0  # 0 表示玩家在走路状态，1 表示骑车状态
    health = 10.0
    pos_screen = (250.0, 600.0)
    speed = 60.0
    speed_dir = [0.0, 0.0]
    player_dir = 0.0

    def update_pos(self, delta_t):
        if not self.speed_dir[0] and not self.speed_dir[1]: return
        x, y = self.pos_screen
        dx, dy = self.speed_dir
        dx, dy = gmath.get_vector(dx, dy)
        sx, sy = self.speed * dx, self.speed * dy
        self.player_dir = gmath.get_dir(dx, dy)
        x += sx * delta_t
        y -= sy * delta_t
        x = max(x, 16)
        x = min(x, 484)
        y = min(y, 784)
        if x <= 16: self.health -= max(-sx / 4000, 0)  # 尝试越界，扣血
        if x >= 484: self.health -= max(sx / 4000, 0)
        if y >= 784: self.health -= max(-sy / 4000, 0)
        if y < 600:
            game.s_dist += 600 - y
            y = 600
        self.pos_screen = (x, y)

    def render(self, screen):
        nskin = skin.player_skin
        nskin = pygame.transform.rotate(nskin, gmath.rad_to_deg(self.player_dir))
        skin_rect = nskin.get_rect()
        skin_rect.center = self.pos_screen
        screen.blit(nskin, skin_rect)

    def get_accurate_speed(self):
        if not self.speed_dir[0] and not self.speed_dir[1]: return 0
        else: return self.speed
