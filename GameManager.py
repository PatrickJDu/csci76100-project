import random
import Config
import Genetic_Algorithm as ga
import numpy as np
import pandas as pd
from Displayer import mainDisplay
from Block import Block
from Snake import Snake
from State import State

# Expectiminimax imports
from EMMPreyAI import emmPreyAI
from EMMHunterAI import emmHunterAI

# Genetic Algorithm import
from GenAI import genAI


# manages the entire game.
class GameManager:
    # handles what the game manager does.
    def __init__(self):
        if Config.aiMode == Config.GENETIC_ALGORITHM:
            self.initGeneticAlgorithm()

        elif Config.aiMode == Config.EXPECTIMINIMAX:
            self.initExpectiminimax()

        # keeps the program alive until game window is closed.
        while Config.showWindow and not mainDisplay.is_closed():
            pass

    # game manager init for genetic algorithm
    def initGeneticAlgorithm(self):
        # training mode
        if Config.ga_mode == 0:

            # randomly initialize first populations/chromosomes
            prey_new_population = np.random.choice(np.arange(-1, 1, step=0.01), size=Config.population_matrix_size,
                                                   replace=True)
            hunter_new_population = np.random.choice(np.arange(-1, 1, step=0.01), size=Config.population_matrix_size,
                                                     replace=True)

            # iterate over each generation
            generation_counter = 0
            for generation in range(Config.num_of_generations):
                prey_fitness = []
                hunter_fitness = []

                # for each chromosome, run game and determine prey & hunter fitness values
                for chromosome in range(Config.chromosomes):
                    score = self.run(1, prey_new_population[chromosome], hunter_new_population[chromosome])[0]
                    print(score)
                    prey_score = ga.prey_score(score)
                    hunter_score = ga.hunter_score(score)
                    prey_fitness.append(prey_score)
                    hunter_fitness.append(hunter_score)

                # convert to array and determine max prey & hunter fitnesses
                prey_fitness = np.array(prey_fitness)
                hunter_fitness = np.array(hunter_fitness)
                max_prey_fitness = np.amax(prey_fitness)
                max_hunter_fitness = np.amax(hunter_fitness)

                # determine prey & hunter parents based on highest fitness values
                prey_parents = ga.select_mating_pool(prey_new_population, prey_fitness, Config.num_of_parents)
                hunter_parents = ga.select_mating_pool(hunter_new_population, hunter_fitness, Config.num_of_parents)

                # determine prey & hunter offsprings using crossover method on selected parents
                prey_offspring_crossover = ga.crossover(prey_parents, offspring_size=(
                Config.population_matrix_size[0] - prey_parents.shape[0], Config.num_w_all))
                hunter_offspring_crossover = ga.crossover(hunter_parents, offspring_size=(
                Config.population_matrix_size[0] - hunter_parents.shape[0], Config.num_w_all))

                # randomly mutate offspring chromosomes to build in gene diversity
                prey_offspring_mutation = ga.mutation(prey_offspring_crossover)
                hunter_offspring_mutation = ga.mutation(hunter_offspring_crossover)

                # create new prey & hunter populations based on selected parents and offspirngs
                prey_new_population[0: prey_parents.shape[0], :] = prey_parents
                prey_new_population[prey_parents.shape[0]:, :] = prey_offspring_mutation
                hunter_new_population[0: hunter_parents.shape[0], :] = hunter_parents
                hunter_new_population[hunter_parents.shape[0]:, :] = hunter_offspring_mutation

                # save prey & hunter populations for future use if at save interval
                generation_counter += 1
                if generation_counter == Config.generation_save_interval:
                    prey_output_file = 'prey_output_gen' + str(generation) + '.csv'
                    hunter_output_file = 'hunter_output_gen' + str(generation) + '.csv'
                    pd.DataFrame(prey_new_population, index=None, columns=None).to_csv(prey_output_file, index=False,
                                                                                       header=False)
                    pd.DataFrame(hunter_new_population, index=None, columns=None).to_csv(hunter_output_file,
                                                                                         index=False, header=False)
                    generation_counter == 0

                # print results from generation
                print('for generation: ' + str(generation) + ', max prey fitness = ' + str(
                    max_prey_fitness) + ', max hunter fitness = ' + str(max_hunter_fitness))

    # game manager init for expectiminimax algorithm goes here
    def initExpectiminimax(self):
        pass

    # creates the first state of a run and returns it.
    def getStartState(self):
        # prey starts at a random position with a length of 1.
        prey_x = random.randint(0, Config.mapSize - 1)
        prey_y = random.randint(0, Config.mapSize - 1)
        prey_head = Block(prey_x, prey_y)

        # hunter starts at the opposite position with a length of 1.
        hunter_x = (prey_x + Config.mapSize // 2 + 1) % Config.mapSize
        hunter_y = (prey_y + Config.mapSize // 2 + 1) % Config.mapSize
        hunter_head = Block(hunter_x, hunter_y)

        # builds the first state and adds in the food at a random available position.
        return State(Config.PREY_TURN, Snake("prey", [prey_head]), Snake("hunter", [hunter_head]))

    # Counts how many times the hunter comes within 2 blocks of the fruit
    # WIP
    def hunter_from_fruit(self, state, count):
        # Grab the x and y of both the fruit and the hunter
        fruit_x, fruit_y = state.food.x, state.food.y
        hunter_x, hunter_y = state.hunter.body[0].x, state.hunter.body[0].y
        # Checking here if the hunter is ever 2 blocks within the fruits territory

        return count

    # run the game n number of times then returns a list of scores of each final state.
    def run(self, numIterations=1, w_prey=[], w_hunter=[]):
        scores = []

        # runs the game n iterations.
        for _ in range(0, numIterations):
            # creates a new start state and begins the game for the iteration.
            state = self.getStartState()

            turn_counter = 0
            while not state.is_final() and turn_counter <= Config.maxSteps:
                # draws the state of the game after both players made their turn.
                if Config.showWindow and turn_counter % 2 == 0 and not mainDisplay.is_closed():
                    mainDisplay.draw(state)

                turn_counter += 1

                # continues playing until it reach a final state.
                # if a final state is met, the loop continues to keep the game window up.
                if not state.is_final():
                    # decides the next action based on the ai mode.
                    if Config.aiMode == Config.EXPECTIMINIMAX:
                        state = self.expectiminimaxApproach(state)
                    else:
                        state = self.geneticAlgorithmApproach(state, w_prey, w_hunter)

                # To give the functionality of closing the window.
                if Config.showWindow and mainDisplay.is_closed():
                    pass

            # draws the last state.
            if Config.showWindow and not mainDisplay.is_closed():
                mainDisplay.draw(state)

            scores.append(state.score())

        return scores

    # returns the next state based on expectiminimax.
    def expectiminimaxApproach(self, state):
        next_state = None
        if state.turn == Config.PREY_TURN:
            next_state = state.next_state(emmPreyAI.getMove(state))
        else:
            next_state = state.next_state(emmHunterAI.getMove(state))

        if next_state is None:
            return state
        return next_state

    # returns the next state based on genetic algorithm.
    def geneticAlgorithmApproach(self, state, w_prey, w_hunter):

        # get next step
        next_state = state.next_state(genAI.getMove(state, w_prey, w_hunter))

        # return next step
        if next_state is None:
            return state
        return next_state


# starts the game.
game = GameManager()