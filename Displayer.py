# this file handles rendering the state in a pygame window.
# unless changes are to be made to the rendering, this file can be ignored.
import pygame
import Config
from Snake import Snake
from State import State

# a singleton class for creating a pygame window and rendering the state of the game.
class Displayer:
    # creates the pygame window.
    def __init__(self):
        self.window = pygame.display.set_mode((Config.windowSize, Config.windowSize))
        self.closed = False

    # checks if the pygame window is closed.
    def is_closed(self):
        if self.closed:
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.closed = True
                    return True

    # draws the state of the game.
    def draw(self, state):
        self.window.fill((0, 0, 0))

        self.draw_food_and_snakes(state)
        self.draw_grid()

        pygame.display.update()
        pygame.time.delay(Config.tickDelay)

    # draws the food and snakes in the state.
    def draw_food_and_snakes(self, state):
        preyHead = (state.prey.head().x, state.prey.head().y)
        hunterHead = (state.hunter.head().x, state.hunter.head().y)

        # iterates through every block in the map and draws them based on what the block represents.
        # prey snake is drawn in green blocks while the hunter snake is drawn in orange blocks.
        # the food is drawn as a blue block.
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

    # draws the grid on the map.
    def draw_grid(self):
        line_clr = (75, 75, 75)
        x = 0
        y = 0

        for _ in range(Config.mapSize):
            x += Config.sizeRatio
            y += Config.sizeRatio
            pygame.draw.line(self.window, line_clr, (x, 0), (x, Config.windowSize))
            pygame.draw.line(self.window, line_clr, (0, y), (Config.windowSize, y))

    # draws a single block at the given position with the specified color.
    def draw_block(self, x, y, clr):
        pygame.draw.rect(self.window, clr, (x * Config.sizeRatio + 1, (Config.mapSize - y - 1) * Config.sizeRatio + 1, Config.sizeRatio - 1, Config.sizeRatio - 1))

    # draws eyes at the given position.
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

# this is used as the singleton instance.
mainDisplay = None

if Config.showWindow:
    mainDisplay = Displayer()