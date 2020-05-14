# this is the configuration file for the project.
# important global variables are defined here.
import sys

# the approach being used for the program. must be either EXPECTIMINIMAX or GENETIC_ALGORITHM.
(EXPECTIMINIMAX, GENETIC_ALGORITHM) = (0, 1)
aiMode = GENETIC_ALGORITHM

# defines a readable variable for the current turn of a state.
(PREY_TURN, HUNTER_TURN) = (0, 1)

# defines readable variables for the directions.
(UP, DOWN, LEFT, RIGHT) = (0, 1, 2, 3)

# size of the game screen and the grid.
windowSize = 800
mapSize = 25
sizeRatio = windowSize // mapSize

# the delay between each rendering of the state. must be an integer.
tickDelay = 2

# maximum number of steps in a single game run
maxSteps = 6000

# genetic algorithm parameters
chromosomes = 50
num_of_generations = 100
num_of_parents = 15
num_w0 = 8
num_w1 = 10
num_w2 = 15
num_w3 = 3
num_w_all = num_w0*num_w1 + num_w1*num_w2 + num_w2*num_w3
population_matrix_size = (chromosomes, num_w_all)
generation_save_interval = 5

# mode to run genetic algorithm. 0 = training, 1 = load population, 2 = load weights. 0 set as default.
ga_mode = 0
input_file = ''
if len(sys.argv) >= 3:
    ga_mode = sys.argv[2]
    if sys.argv[2] == '1' or sys.argv[2] == '2':
        input_file = sys.argv[3]

# set to 0 to play the game with the window hidden
showWindow = True
if len(sys.argv) >= 2 and sys.argv[1] == '0':
    showWindow = False