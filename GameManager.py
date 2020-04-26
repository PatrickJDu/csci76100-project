import random

import pygame
from Snake import Snake
from Cube import Cube

w = 800
rows = 25
s = Snake((0, 255, 0), (10, 10))


def draw_grid(surface):
    line_btwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x += line_btwn
        y += line_btwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redraw_window(surface, food):
    global w, rows, s
    surface.fill((0, 0, 0))
    s.draw(surface)
    food.draw(surface)
    draw_grid(surface)
    pygame.display.update()


def fruit(item):
    global rows
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # This avoids putting the fruit on top of the snake
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y


def message_box(subject, content):
    pass


def main():
    global w, rows, s

    win = pygame.display.set_mode((w, w))

    clock = pygame.time.Clock()
    flag = True
    food = Cube(fruit(s), color=(255, 0, 0))

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == food.pos:
            s.add_cube()
            food = Cube(fruit(s), color=(255, 0, 0))
        for x in range(len(s.body)):
            # Check for collision on own body
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                s.reset((10,10))
                break
        redraw_window(win, food)


main()
