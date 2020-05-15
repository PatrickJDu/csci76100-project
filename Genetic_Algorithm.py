#Genetic algorithm module
import numpy as np
import random
from random import choice, randint

#Functio to determine fitness of prey
def prey_score(score):
    return score*100

#Function to Determine fitness of hunter
def hunter_score(score):
    return (4000 - score*100)

#Function to select parents for 'breeding' based on fitness values
def select_mating_pool(pop, fitness, num_parents):
    parents = np.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999
    return parents

#Function to create offsprings based on selected parents
def crossover(parents, offspring_size): 
    offspring = np.empty(offspring_size)
    
    for k in range(offspring_size[0]): 
        while True:
            parent1_idx = random.randint(0, parents.shape[0] - 1)
            parent2_idx = random.randint(0, parents.shape[0] - 1)
            # produce offspring from two parents if they are different
            if parent1_idx != parent2_idx:
                for j in range(offspring_size[1]):
                    if random.uniform(0, 1) < 0.5:
                        offspring[k, j] = parents[parent1_idx, j]
                    else:
                        offspring[k, j] = parents[parent2_idx, j]
                break
    return offspring

#Function to build in random mutation in selected offspring to maintain population variation
def mutation(offspring_crossover):
    
    for idx in range(offspring_crossover.shape[0]):
        for _ in range(25):
            i = randint(0,offspring_crossover.shape[1]-1)

        random_value = np.random.choice(np.arange(-1,1,step=0.001),size=(1),replace=False)
        offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value

    return offspring_crossover
