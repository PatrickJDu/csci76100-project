# this is the configuration file for the project.
# important global variables are defined here.
import sys

# the approach being used for the program. must be either EXPECTIMINIMAX or GENETIC_ALGORITHM.
(EXPECTIMINIMAX, GENETIC_ALGORITHM) = (0, 1)
aiMode = GENETIC_ALGORITHM
#if len(sys.argv) == 1:
#    aiMode = GENETIC_ALGORITHM
#else:
#    aiMode = sys.argv[1]

# defines a readable variable for the current turn of a state.
(PREY_TURN, HUNTER_TURN) = (0, 1)

# defines readable variables for the directions.
(UP, DOWN, LEFT, RIGHT) = (0, 1, 2, 3)

# size of the game screen and the grid.
windowSize = 800
mapSize = 25
mapCenter1 = mapSize // 2
mapCenter2 = mapSize - mapCenter1
sizeRatio = windowSize // mapSize

# the delay between each rendering of the state. must be an integer.
tickDelay = 5

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
input_file_prey = ''
input_file_hunter = ''
if len(sys.argv) >= 4:
    ga_mode = int(sys.argv[3])
    if sys.argv[3] == '1' or sys.argv[3] == '2':
        input_file_prey = sys.argv[4]
        input_file_hunter = sys.argv[5]

# genetic algorithm training mode. 0 = train both prey & hunter, 1 = train prey, 2 = train hunter. 0 set as default.
ga_training_mode = 0
if len(sys.argv) >= 5:
    ga_training_mode = int(sys.argv[4])

# set to 0 to play the game with the window hidden
showWindow = True
if len(sys.argv) >= 3 and sys.argv[2] == '0':
    showWindow = False

#GameManager.py (EXPECTIMINIMAX/GENETIC_ALGORITHM) (DISPLAY_ON/DISPLAY_OFF) (TRAIN/LOAD_POPULATION/LOAD_WEIGHT) (TRAIN BOTH/PREY/HUNTER or LOAD_PREY) (LOAD_HUNTER)
