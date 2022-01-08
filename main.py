import pygame as pg
import os
import sys
from random import randint

hero_group = pg.sprite.Group()
meteor_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
wight, height = size = 600, 700


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pg.sprite.Sprite):
    def __init__(self, level):
        super().__init__(hero_group)
        self.v = 9
        self.image = load_image('player.png')
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.y = height - self.size[1]
        self.rect.x = (wight - self.size[0]) // 2
        self.generate_params(level)
        self.mask = pg.mask.from_surface(self.image)

    def generate_params(self, lvl):
        if lvl == 3:
            self.v = 9
        elif lvl == 2:
            self.v = 9

    def move_r(self):
        if self.rect.x + self.v <= wight - self.size[0]:
            self.rect.x += self.v

    def move_l(self):
        if self.rect.x - self.v >= 0:
            self.rect.x -= self.v


class Meteor(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(meteor_group)
        self.image = load_image('meteor.png')
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.y = randint(-3 * self.size[-1], -self.size[1])
        self.rect.x = randint(0, wight - self.size[0])
        self.vx = randint(-4, 4)
        self.vy = randint(5, 9)
        self.collides_count = 0
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.x > wight or self.rect.x < -self.size[0] or self.rect.y > size[1] + self.size[1]:
            self.rect.y = randint(-3 * self.size[-1], -self.size[1])
            self.rect.x = randint(0, wight - self.size[0])
            self.vx = randint(-4, 4)
            self.vy = randint(5, 10)
        if pg.sprite.collide_mask(self, player):
            self.collides_count += 1
            if self.collides_count >= 3:
                print('dead')
        else:
            self.collides_count = 0


class Bullet:
    def __init__(self):
        super().__init__(bullet_group)
        self.image = load_image('bullet.png')


def main():
    screen = pg.display.set_mode((1000, 480))
    font_input = pg.font.Font(None, 32)
    input_box = pg.Rect(555, 5, 140, 32)
    level_1_text = pg.font.Font(None, 40)
    level_2_text = pg.font.Font(None, 40)
    level_3_text = pg.font.Font(None, 40)
    level_1_box = pg.Rect(10, 50, 32, 32)
    level_2_box = pg.Rect(10, 92, 32, 32)
    level_3_box = pg.Rect(10, 134, 32, 32)
    clock = pg.time.Clock()
    color_inactive = pg.Color('lightskyblue3')

    color_active = pg.Color('dodgerblue2')
    manual = pg.font.Font(None, 32)
    text_manual = 'Press here input your nickname and press Enter -->'
    color = color_inactive
    active = False
    text = ''
    nick = 'NoName'
    running = False
    while not running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                if level_1_box.collidepoint(event.pos):
                    start_game(1)
                if level_2_box.collidepoint(event.pos):
                    start_game(2)
                if level_3_box.collidepoint(event.pos):
                    start_game(3)
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        if text:
                            nick = text
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 34:
                            text += event.unicode
        screen.fill((30, 30, 30))
        txt_surface = font_input.render(text, True, color)
        manual_r = manual.render(text_manual, True, color_inactive)
        lvl1 = level_1_text.render('Level 1', True, color_inactive)
        lvl2 = level_2_text.render('Level 2', True, color_inactive)
        lvl3 = level_3_text.render('Level 3', True, color_inactive)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(manual_r, (10, 10))
        screen.blit(lvl1, (50, 50))
        screen.blit(lvl2, (50, 92))
        screen.blit(lvl3, (50, 134))
        pg.draw.rect(screen, color, input_box, 2)
        pg.draw.rect(screen, pg.Color('green'), level_1_box)
        pg.draw.rect(screen, pg.Color('yellow'), level_2_box)
        pg.draw.rect(screen, pg.Color('red'), level_3_box)
        pg.display.flip()
        clock.tick(30)


def start_game(lvl):
    global player
    clock = pg.time.Clock()
    running = True
    fps = 60
    screen = pg.display.set_mode(size)
    player = Player(lvl)
    go_left, go_right = False, False
    # left_top = (-meteor_image_size[0], -meteor_image_size[1])
    # right_top = (screen.get_size()[0] + meteor_image_size[0], -meteor_image_size[1])
    # right_bottom = (screen.get_size()[0] + meteor_image_size[0], screen.get_size()[1] + meteor_image_size[1])
    # left_bottom = (-meteor_image_size[0], screen.get_size()[1] + meteor_image_size[1])
    for i in range(lvl * 3):
        Meteor()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    go_left = True
                elif event.key == pg.K_RIGHT:
                    go_right = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    go_left = False
                elif event.key == pg.K_RIGHT:
                    go_right = False
        if go_right:
            player.move_r()
        if go_left:
            player.move_l()

        screen.fill((255, 255, 255))
        hero_group.draw(screen)
        meteor_group.draw(screen)
        meteor_group.update()
        clock.tick(fps)
        pg.display.flip()

if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()