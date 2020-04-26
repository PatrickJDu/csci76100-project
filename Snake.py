import math
import random
import pygame
from Cube import Cube
import SnakeAI

right_arrow = pygame.event.Event(pygame.KEYDOWN, {'key': 275, 'mod': 0, 'unicode': '', 'scancode': 77})
left_arrow = pygame.event.Event(pygame.KEYDOWN, {'key': 276, 'mod': 0, 'unicode': '', 'scancode': 75})
up_arrow = pygame.event.Event(pygame.KEYDOWN, {'key': 273, 'mod': 0, 'unicode': '', 'scancode': 72})
down_arrow = pygame.event.Event(pygame.KEYDOWN, {'key': 274, 'mod': 0, 'unicode': '', 'scancode': 80})


class Snake:
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        # Check if we quit the ui
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # Random move
        # Turns aren't being plugged inot the dictionary correctly. Have to figure out why manually entering in key
        # doesn't cause this issue but randomizing like this causes this issue
            elif event.type == pygame.KEYDOWN:
                choice = SnakeAI.player_move()
                if choice == pygame.K_LEFT:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif choice == pygame.K_RIGHT:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif choice == pygame.K_DOWN:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif choice == pygame.K_UP:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        pygame.event.post(right_arrow)
        pygame.event.post(left_arrow)
        pygame.event.post(up_arrow)
        pygame.event.post(down_arrow)
        # Makes sure to update body of snake as it turns
        for i, c in enumerate(self.body):
            p = c.pos[:]
            # print("P: " + str(p))
            # print("turns: " + str(self.turns))
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            # If it doesn't turn make sure if it goes pass the borders to appear on the other side.
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # We need to know which side of the snake to add the cube to.
        # So we check what direction we are currently moving in to determine if we
        # need to add the cube to the left, right, above or below.
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))
        # Make sure the tail is moving in the same direction
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
