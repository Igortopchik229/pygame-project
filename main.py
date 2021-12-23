import pygame as pg
import sys
import os


class Player:
    def __init__(self, hp, v):
        self.hp = hp
        self.v = v


class Bullet:
    def __init__(self, v):
        self.v = v


class Meteor:
    def __init__(self, hp):
        self.hp = hp


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
    if lvl == 1:
        pass
    elif lvl == 2:
        pass
    else:
        pass
    print(lvl)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()