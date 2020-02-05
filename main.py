import pygame as pg

pg.init()
win_width = 800
win_height = 600
root = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("Jiri's fun stuff")

player_img = pg.image.load('spaceship.png')
px = 368
py = 440
px_speed = 0
py_speed = 0
ship_speed = 0.2

def player(x, y):
    root.blit(player_img, (x, y))

play = True
while play:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            play = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                px_speed = -ship_speed
            if event.key == pg.K_RIGHT:
                px_speed = +ship_speed
            if event.key == pg.K_UP:
                py_speed = -ship_speed
            if event.key == pg.K_DOWN:
                py_speed = ship_speed
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                px_speed = 0
            if event.key == pg.K_UP or  event.key == pg.K_DOWN:
                py_speed = 0
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    root.fill((0, 0, 0))

    px += px_speed
    py += py_speed
    if px < 0:
        px = 0
    elif px > win_width - 64:
        px = win_width - 64
    if py < 0:
        py = 0
    elif py > win_height - 64:
        py = win_height - 64
    player(px, py)
    pg.display.update()