import pygame
import random
snake_block = 10
snake_speed = 15

action_dict = {
    0: pygame.K_LEFT,
    1: pygame.K_RIGHT,
    2: pygame.K_UP,
    3: pygame.K_DOWN
}


def player_move():
    choice = random.choice(action_dict)
    return choice