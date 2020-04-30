# pygame is used to display the game
import pygame
import Config
from Snake import Snake
from State import State

class Displayer:
    def create_window(self):
        self.window = pygame.display.set_mode((Config.windowSize, Config.windowSize))
        self.closed = False

    def is_closed(self):
        if self.closed:
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.closed = True
                    break

    def draw(self, state):
        self.window.fill((0, 0, 0))
        self.draw_grid()

        preyHead = (state.prey.head().x, state.prey.head().y)
        hunterHead = (state.hunter.head().x, state.hunter.head().y)
        for i in range(0, Config.mapSize):
            for j in range(0, Config.mapSize):
                blockNum = state.map[i][j]
                if blockNum == 1:
                    self.draw_block(i, j, (0, 125, 255))
                elif blockNum == 2:
                    self.draw_block(i, j, (0, 255, 125))
                    if preyHead == (i, j):
                        self.draw_eyes(i, j)
                elif blockNum == 3:
                    self.draw_block(i, j, (255, 125, 0))
                    if hunterHead == (i, j):
                        self.draw_eyes(i, j)
                elif blockNum == 4:
                    self.draw_block(i, j, (255, 0, 0))
                    self.draw_eyes(i, j)

        pygame.display.update()
        if state.is_final():
            pygame.time.delay(Config.tickDelay*10)
        else:
            pygame.time.delay(Config.tickDelay)

    def draw_grid(self):
        line_clr = (75, 75, 75)
        x = 0
        y = 0

        for _ in range(Config.mapSize):
            x += Config.sizeRatio
            y += Config.sizeRatio
            pygame.draw.line(self.window, line_clr, (x, 0), (x, Config.windowSize))
            pygame.draw.line(self.window, line_clr, (0, y), (Config.windowSize, y))

    def draw_block(self, x, y, clr):
        pygame.draw.rect(self.window, clr, (x * Config.sizeRatio + 1, (Config.mapSize - y - 1) * Config.sizeRatio + 1, Config.sizeRatio - 1, Config.sizeRatio - 1))
    
    def draw_eyes(self, x, y):
        center = Config.sizeRatio // 2
        radius = Config.sizeRatio // 6
        eye_dist = Config.sizeRatio // 4 + 1

        eye1 = (x * Config.sizeRatio + center - eye_dist, (Config.mapSize - y - 1) * Config.sizeRatio + center)
        eye2 = (x * Config.sizeRatio + center + eye_dist, (Config.mapSize - y - 1) * Config.sizeRatio + center)
        pupil_offset = Config.sizeRatio//30 + 1

        pygame.draw.circle(self.window, (50, 50, 50), eye1, radius)
        pygame.draw.circle(self.window, (255, 255, 255), eye1, radius - pupil_offset)
        pygame.draw.circle(self.window, (50, 50, 50), eye2, radius)
        pygame.draw.circle(self.window, (255, 255, 255), eye2, radius - pupil_offset)

mainDisplay = Displayer()