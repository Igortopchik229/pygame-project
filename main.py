import pygame as pg
import os
import sys
from random import randint, choice

hero_group = pg.sprite.Group()  # sprite group for player
meteor_group = pg.sprite.Group()  # sprite group for meteorites
bullet_group = pg.sprite.Group()  # sprite group for meteorites
stars = pg.sprite.Group()  # sprite group for stars(animation)
screen = pg.display.set_mode((1000, 480))  # start menu window
wight, height = size = 600, 700  # display size for game
paused = 0  # flag for pause
nick = 'NoName'  # default nick
score_now = 0  # score
game_end = 0  # flag for detect lose


def load_image(name, colorkey=None):  # function for load image
    fullname = os.path.join('data', name)
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
        self.v = 7  # speed
        self.image = load_image('player.png')  # player image
        self.rect = self.image.get_rect()  # player rect
        self.size = self.image.get_size()  # size image
        self.rect.y = height - self.size[1]  # start position y
        self.rect.x = (wight - self.size[0]) // 2  # start position x
        self.mask = pg.mask.from_surface(self.image)  # image mask

    def move_r(self):  # move right
        if self.rect.x + self.v <= wight - self.size[0]:
            self.rect.x += self.v

    def move_l(self):  # move left
        if self.rect.x - self.v >= 0:
            self.rect.x -= self.v

    def move_u(self):  # move up
        if self.rect.y - self.v >= 0:
            self.rect.y -= self.v

    def move_d(self):  # move down
        if self.rect.y + self.v <= height - self.size[1]:
            self.rect.y += self.v

    def update(self):  # kill player sprite if game end == 1
        if game_end:
            self.kill()


class Meteor(pg.sprite.Sprite):
    def __init__(self, level):
        super().__init__(meteor_group)
        self.level = level  # level
        self.image = load_image('meteor.png')  # meteorite image
        self.rect = self.image.get_rect()  # size image
        self.size = self.image.get_size()  # rect size
        self.rect.y = randint(-3 * self.size[-1], -self.size[1])  # start position y
        self.rect.x = randint(0, wight - self.size[0])  # start position x
        self.vx = randint(-4, 4)  # speed x
        self.vy = randint(5, 10)  # speed y
        self.collides_count_player = 0  # collides with player
        self.collides_count_bullet = 0  # collides with bullet
        self.mask = pg.mask.from_surface(self.image)  # mask image

    def new_meteor(self):  # respawn meteorite
        self.rect.y = -self.size[1]  # start position y
        self.rect.x = randint(0, wight - self.size[0])  # start position x
        self.vx = randint(-4, 4)
        self.vy = randint(5, 10)

    def update(self):
        global game_end, score_now
        self.rect.x += self.vx  # move x
        self.rect.y += self.vy  # move y
        if self.rect.x > wight or self.rect.x < -self.size[0] or self.rect.y > size[1] + self.size[1]:
            self.new_meteor()  # if meteor not on display
        if pg.sprite.collide_mask(self, player):  # collide with player
            self.collides_count_player += 1
            if self.collides_count_player == 2:  # if 2 collides with player
                game_end = 1  # lose
        else:
            self.collides_count_player = 0
        if pg.sprite.spritecollide(self, bullet_group, False):  # collide with bullet group
            self.collides_count_bullet += 1
            if self.collides_count_bullet == 2:
                pg.sprite.spritecollide(self, bullet_group, True)  # destroy bullet
                score_now += 1
                self.collides_count_bullet = 0
                self.new_meteor()  # respawn meteor
        else:
            self.collides_count_bullet = 0


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(bullet_group)
        self.image = load_image('bullet.png')  # bullet image
        self.size = self.image.get_size()  # image size
        self.rect = self.image.get_rect()  # rect
        self.rect.x = pos[0]  # start position x
        self.rect.y = pos[1] - self.size[1]  # start position y
        self.vy = 8  # speed
        self.mask = pg.mask.from_surface(self.image)  # image mask

    def update(self):
        if self.rect.y - self.vy > -self.size[1]:  # if bullet on display
            self.rect.y -= self.vy  # move up
        else:
            self.kill()  # destroy bullet


class Particle(pg.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pg.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(stars)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.05

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if self.rect.y > height:
            self.kill()


def main():
    global nick, screen  # global nick name, screen
    pg.display.set_caption('spaceship vs meteorites')  # caption
    screen = pg.display.set_mode((1000, 200))  # screen menu
    font_input = pg.font.Font(None, 32)  # font input
    input_box = pg.Rect(430, 5, 140, 32)  # input box
    level_1_text = pg.font.Font(None, 40)  # font lvl1
    level_2_text = pg.font.Font(None, 40)  # font lvl2
    level_3_text = pg.font.Font(None, 40)  # font lvl3
    level_1_box = pg.Rect(10, 50, 32, 32)  # level1 button
    level_2_box = pg.Rect(10, 100, 32, 32)  # level2 button
    level_3_box = pg.Rect(10, 150, 32, 32)  # level 3 button
    clock = pg.time.Clock()
    color_inactive = pg.Color('lightskyblue3')  # color input box not active
    file = open('scores.txt', 'r', encoding='utf8')  # open score file

    # work with text and file
    scores = file.readlines()
    level_1_score = scores[0].split(' ')
    level_2_score = scores[1].split(' ')
    level_3_score = scores[2].split(' ')
    level_1_score = (' '.join(level_1_score[:-1]), level_1_score[-1])
    level_2_score = (' '.join(level_2_score[:-1]), level_2_score[-1])
    level_3_score = (' '.join(level_3_score[:-1]), level_3_score[-1][:-1])
    file.close()
    level_1_score_name = pg.font.Font(None, 40)
    level_2_score_name = pg.font.Font(None, 40)
    level_3_score_name = pg.font.Font(None, 40)
    color_active = pg.Color('dodgerblue2')
    manual_nick = pg.font.Font(None, 32)
    text_manual = 'Press here and input your nickname -->'

    color = color_inactive
    active = False  # flag input box active
    text = ''  # input text
    nick = 'NoName'  # default nick
    stop = False
    while not stop:  # menu cycle
        for event in pg.event.get():  # check events
            if event.type == pg.QUIT:  # if close window
                stop = True  # stop
            if event.type == pg.MOUSEBUTTONDOWN:  # if mouse click
                if input_box.collidepoint(event.pos):  # if mouse click in input box
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                if level_1_box.collidepoint(event.pos):  # if click on lvl1
                    return 1
                if level_2_box.collidepoint(event.pos):  # if click on lvl2
                    return 2
                if level_3_box.collidepoint(event.pos):  # if click on lvl3
                    return 3
            if event.type == pg.KEYDOWN:  # if key down
                if active:
                    if event.key == pg.K_BACKSPACE:  # delete last sym from text
                        text = text[:-1]
                    elif event.key == pg.K_RETURN:  # if enter
                        color = color_inactive
                        active = False  # input box not active
                    else:
                        if len(text) < 32:  # max len nick 33
                            text += event.unicode  # change text
                            nick = text
        screen.fill((30, 30, 30))  # gray color
        txt_surface = font_input.render(text, True, color)  # render text
        manual_r = manual_nick.render(text_manual, True, color_inactive)  # render text
        lvl1 = level_1_text.render('Level 1', True, color_inactive)  # render text
        lvl2 = level_2_text.render('Level 2', True, color_inactive)  # render text
        lvl3 = level_3_text.render('Level 3', True, color_inactive)  # render text
        lvl1name = level_1_score_name.render(f'Leader: {level_1_score[0]} | points: {level_1_score[1][:-1]}',
                                             True, color_inactive)  # render text
        lvl2name = level_2_score_name.render(f'Leader: {level_2_score[0]} | points: {level_2_score[1][:-1]}',
                                             True, color_inactive)  # render text
        lvl3name = level_3_score_name.render(f'Leader: {level_3_score[0]} | points: {level_3_score[1]}',
                                             True, color_inactive)  # render text
        width = max(200, txt_surface.get_width()+10)  # change width input box if nick don't fit
        input_box.w = width

        # show text and buttons
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(manual_r, (10, 10))
        screen.blit(lvl1, (50, 50))
        screen.blit(lvl2, (50, 100))
        screen.blit(lvl3, (50, 150))
        screen.blit(lvl1name, (150, 50))
        screen.blit(lvl1name, (150, 50))
        screen.blit(lvl2name, (150, 100))
        screen.blit(lvl3name, (150, 150))
        pg.draw.rect(screen, color, input_box, 2)
        pg.draw.rect(screen, pg.Color('green'), level_1_box)
        pg.draw.rect(screen, pg.Color('yellow'), level_2_box)
        pg.draw.rect(screen, pg.Color('red'), level_3_box)

        pg.display.flip()
        clock.tick(30)


def start_game(lvl):
    global player, paused, screen  # global player, pause
    clock = pg.time.Clock()
    running = True
    fps = 60  # fps
    screen = pg.display.set_mode(size)  # screen game size
    player = Player(lvl)  # player
    reload_1_bullet = pg.time.get_ticks()
    bullets = 3 * lvl  # bullet count on lvl
    bullets_text = pg.font.Font(None, 40)  # bullet font
    score_text = pg.font.Font(None, 40)  # score font
    animation_start = 0  # start animation flag
    background = load_image('background.png')  # background image
    go_left, go_right, go_up, go_down = False, False, False, False  # flag to move
    for i in range(lvl * 4):  # generate meteorites on lvl
        Meteor(lvl)
    while running:
        if not paused and not game_end:  # if not paused and not lose
            if (pg.time.get_ticks() - reload_1_bullet) // 500 and bullets < 3 * lvl + 1:  # reload bullet
                reload_1_bullet = pg.time.get_ticks()
                bullets += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                # moves with arrows
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT:
                        go_left = False
                    if event.key == pg.K_RIGHT:
                        go_right = False
                    if event.key == pg.K_UP:
                        go_up = False
                    if event.key == pg.K_DOWN:
                        go_down = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        go_left = True
                    if event.key == pg.K_RIGHT:
                        go_right = True
                    if event.key == pg.K_UP:
                        go_up = True
                    if event.key == pg.K_DOWN:
                        go_down = True

                    # shoot
                    if event.key == pg.K_SPACE:
                        if bullets:
                            Bullet((player.rect.x + player.size[0] // 2, player.rect.y))
                            bullets -= 1
                    if event.key == pg.K_p:
                        paused = (paused + 1) % 2

            # move
            if go_right:
                player.move_r()
            if go_left:
                player.move_l()
            if go_up:
                player.move_u()
            if go_down:
                player.move_d()

            screen.blit(background, (0, 0))  # background
            hero_group.draw(screen)  # draw sprites
            meteor_group.draw(screen)  # draw sprites
            bullet_group.draw(screen)  # draw sprites
            bullet_group.update()  # update sprites
            meteor_group.update()  # update sprites

            # show and render text
            text_bullets = bullets_text.render(f'bullet count {bullets}', True, pg.Color('white'))
            text_score = score_text.render(f'points {score_now}', True, pg.Color('white'))
            screen.blit(text_bullets, (10, 10))
            screen.blit(text_score, (10, 55))
            clock.tick(fps)
            pg.display.flip()
        elif game_end:  # if lose
            if not animation_start:
                animation_start = pg.time.get_ticks()  # start animation time
                numbers = range(-5, 6)
                for _ in range(score_now * 5):  # stars count
                    Particle((wight // 2, height // 2), choice(numbers), choice(numbers))
            if (pg.time.get_ticks() - animation_start) // 1000 > 4:  # finish animation (4 sec)
                return screen
            screen.blit(background, (0, 0))
            text_bullets = bullets_text.render(f'bullet count {bullets}', True, pg.Color('white'))
            text_score = score_text.render(f'points {score_now}', True, pg.Color('white'))
            stars.update()
            meteor_group.draw(screen)
            hero_group.draw(screen)
            screen.blit(text_bullets, (10, 10))
            screen.blit(text_score, (10, 55))
            stars.draw(screen)
            clock.tick(fps)
            pg.display.flip()
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                # move
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        paused = (paused + 1) % 2
                    if event.key == pg.K_LEFT:
                        go_left = True
                    if event.key == pg.K_RIGHT:
                        go_right = True
                    if event.key == pg.K_UP:
                        go_up = True
                    if event.key == pg.K_DOWN:
                        go_down = True
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT:
                        go_left = False
                    if event.key == pg.K_RIGHT:
                        go_right = False
                    if event.key == pg.K_UP:
                        go_up = False
                    if event.key == pg.K_DOWN:
                        go_down = False


def game_over(scr, lvl, screen):
    global nick
    if not nick:  # if nick == ''
        nick = 'NoName'
    file = open('scores.txt', 'r', encoding='utf8')  # open file with score
    lines = file.readlines()
    if int(lines[lvl - 1].split()[-1]) < scr:
        lines[lvl - 1] = nick + ' ' + str(scr) + '\n'
    file.close()
    file = open('scores.txt', 'w+', encoding='utf8')  # write new file with record
    file.write(lines[0])
    file.write(lines[1])
    file.write(lines[2])
    file.close()
    running = True
    text_try_again = pg.font.Font(None, 40)
    tta = text_try_again.render('Try again', True, pg.Color('white'))
    box_try_again = pg.Rect(wight // 2 - tta.get_size()[0] // 2 - 3, height // 2 - tta.get_size()[1] // 2 - 3,
                            tta.get_size()[0] + 6, tta.get_size()[1] + 6)  # button try again
    text_go_menu = pg.font.Font(None, 40)
    tga = text_go_menu.render('Go menu', True, pg.Color('white'))
    box_go_menu = pg.Rect(wight // 2 - tga.get_size()[0] // 2 - 3, height // 2 - tga.get_size()[1] // 2 - 3 + 50,
                            tga.get_size()[0] + 6, tga.get_size()[1] + 6)  # button go menu
    text_exit = pg.font.Font(None, 40)
    te = text_exit.render('Close game', True, pg.Color('white'))
    box_exit = pg.Rect(wight // 2 - te.get_size()[0] // 2 - 3, height // 2 - te.get_size()[1] // 2 - 3 + 100,
                            te.get_size()[0] + 6, te.get_size()[1] + 6)  # button close game

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if box_try_again.collidepoint(event.pos):
                    return 1
                if box_go_menu.collidepoint(event.pos):
                    return 2
                if box_exit.collidepoint(event.pos):
                    return 3

        # show buttons
        pg.draw.rect(screen, pg.Color('white'), box_exit, 3)
        pg.draw.rect(screen, pg.Color('white'), box_go_menu, 3)
        pg.draw.rect(screen, pg.Color('white'), box_try_again, 3)

        # show text
        screen.blit(tta, (wight // 2 - tta.get_size()[0] // 2, height // 2 - tta.get_size()[1] // 2))
        screen.blit(tga, (wight // 2 - tga.get_size()[0] // 2, height // 2 - tga.get_size()[1] // 2 + 50))
        screen.blit(te, (wight // 2 - te.get_size()[0] // 2, height // 2 - te.get_size()[1] // 2 + 100))

        pg.display.flip()


def update_sprites():  # clear all sprites, score, flags
    global hero_group, meteor_group, bullet_group, paused, score_now, game_end
    hero_group = pg.sprite.Group()
    meteor_group = pg.sprite.Group()
    bullet_group = pg.sprite.Group()
    paused = 0
    score_now = 0
    game_end = 0


def check_type(obj):  # check that fucn return None
    if obj == None:
        pg.quit()
        quit()


if __name__ == '__main__':
    pg.init()
    close = False
    lvl = main()
    check_type(lvl)
    screen = start_game(lvl)
    check_type(screen)
    mode = game_over(score_now, lvl, screen)
    while not close:
        if mode == 1:  # mode 1 try again
            update_sprites()
            screen = start_game(lvl)
            check_type(screen)
            mode = game_over(score_now, lvl, screen)
            check_type(mode)
        elif mode == 2:  # mode 2 go menu
            update_sprites()
            lvl = main()
            check_type(lvl)
            screen = start_game(lvl)
            check_type(screen)
            mode = game_over(score_now, lvl, screen)
            check_type(mode)
        else:  # mode 3 close game
            close = True
    pg.quit()
