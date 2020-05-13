# this is the configuration file for the project.
# important global variables are defined here.
import sys

# the approach being used for the program. must be either EXPECTIMINIMAX or GENETIC_ALGORITHM.
(EXPECTIMINIMAX, GENETIC_ALGORITHM) = (0, 1)
aiMode = EXPECTIMINIMAX

# defines a readable variable for the current turn of a state.
(PREY_TURN, HUNTER_TURN) = (0, 1)

# defines readable variables for the directions.
(UP, DOWN, LEFT, RIGHT) = (0, 1, 2, 3)

# size of the game screen and the grid.
windowSize = 800
mapSize = 10
sizeRatio = windowSize // mapSize

# the delay between each rendering of the state. must be an integer.
tickDelay = 100

# the amount of iterations to run the game.
numIterations = 1
if len(sys.argv) >= 2:
    numIterations = max(int(sys.argv[1]), 1)
