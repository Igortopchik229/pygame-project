import pygame as pg


def main():
    screen = pg.display.set_mode((1000, 480))
    font_input = pg.font.Font(None, 32)
    input_box = pg.Rect(555, 5, 140, 32)
    clock = pg.time.Clock()
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    manual = pg.font.Font(None, 32)
    text_manual = 'Press here input your nickname and press Enter -->'
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 34:
                            text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font_input.render(text, True, color)
        manual_r = manual.render(text_manual, True, color_inactive)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(manual_r, (10, 10))
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()