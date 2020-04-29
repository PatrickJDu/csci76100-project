import pygame
import random

action_dict = {
    0: pygame.K_LEFT,
    1: pygame.K_RIGHT,
    2: pygame.K_UP,
    3: pygame.K_DOWN
}


def player_move():
    choice = random.choice(action_dict)
    return choice
