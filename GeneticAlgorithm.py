#Genetic algorithm module
import numpy as np
import random
from random import choice, randint

#Function to determine fitness of prey
def prey_score(score, final_state_flag):
    score_offset = 0
    #Hunter killed prey
    if final_state_flag == 1:
        score_offset += -200
    #Prey killed itself
    if final_state_flag == 4:
        score_offset += -500
    return (score*300 + score_offset)

#Function to Determine fitness of hunter
def hunter_score(score, hunter_near_fruit, final_state_flag):
    score_offset = 0
    #Hunter killed prey
    if final_state_flag == 1:
        score_offset += 2000
    #Hunter killed itself
    if final_state_flag == 3:
        score_offset += -500
    return (6000 - score*50 + score_offset - hunter_near_fruit*5)

#Function to select parents for 'breeding' based on fitness values
def select_parents(population, fitness, num_parents):
    #Array to store parents
    parents = np.empty((num_parents, population.shape[1]))
    #For each parent
    for i in range(num_parents):
        #Pick the fittest parent
        max_fitness = np.where(fitness == np.max(fitness))
        max_fitness = max_fitness[0][0]
        #Add parent to parent's list
        parents[i, :] = population[max_fitness, :]
        #Set fitness = negative infinity to avoid picking same parent again
        fitness[max_fitness] = -99999999
    return parents

#Function to create offsprings based on selected parents
def breed(parents, offspring_size): 
    offspring = np.empty(offspring_size)
    for i in range(offspring_size[0]):
        #Continue untill all offsprings are created 
        while True:
            #Randomly pick parents
            parent_1 = random.randint(0, parents.shape[0] - 1)
            parent_2 = random.randint(0, parents.shape[0] - 1)
            # produce offspring from two parents if they are different
            if parent_1 != parent_2:
                for j in range(offspring_size[1]):
                    #Determine which parent to copy gene's from
                    if random.uniform(0, 1) < 0.5:
                        offspring[i, j] = parents[parent_1, j]
                    else:
                        offspring[i, j] = parents[parent_2, j]
                break
    return offspring

#Function to build in random mutation in selected offspring to maintain population variation
def mutate(offspring_crossover):
    num_of_genes_to_mutate = 25
    #Randomly mutate each offspring
    for i in range(offspring_crossover.shape[0]):
        #Try to randomly mutate num_of_genes_to_mutate genes
        for j in range(num_of_genes_to_mutate):
            #Pick gene #
            rand_num = randint(0, offspring_crossover.shape[1] - 1)
        #Pick mutation increment
        random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size=(1), replace = False)
        #Add mutation
        offspring_crossover[i, rand_num] = offspring_crossover[i, rand_num] + random_value

    return offspring_crossover
