#Next move prediction based on genetic algorithm
import random
import math
import Config
from State import State
import numpy as np
from BaseAI import BaseAI
from State import State
from Block import Block
import NeuralNet as nn

#Function to detemrine adjacent block based on a given block
def direction_blocks(current_x, current_y, direction, map_size):

    dir_front_block = []
    dir_left_block = []
    dir_right_block = []

    #Determine coordinates of adjacent blocks
    if current_y == map_size - 1:
        up_block_y = 0
    else:
        up_block_y = current_y + 1

    if current_y == 0:
        down_block_y = map_size - 1
    else:
        down_block_y = current_y - 1

    if current_x == map_size - 1:
        right_block_x = 0
    else:
        right_block_x = current_x + 1

    if current_x == 0:
        left_block_x = map_size - 1
    else:
        left_block_x = current_x - 1

    #Determine adjacent blocks
    up_block = (current_x, up_block_y)
    down_block = (current_x, down_block_y)
    left_block = (left_block_x, current_y)
    right_block = (right_block_x, current_y)

    #Set adjacent blocks based on current direction
    if direction == 0:
        dir_front_block = up_block
        dir_left_block = left_block
        dir_right_block = right_block

    elif direction == 1:
        dir_front_block = down_block
        dir_left_block = right_block
        dir_right_block = left_block

    elif direction == 2:
        dir_front_block = left_block
        dir_left_block = down_block
        dir_right_block = up_block

    else:
        dir_front_block = right_block
        dir_left_block = up_block
        dir_right_block = down_block
    
    return (dir_front_block, dir_left_block, dir_right_block)

#Function to determine angle and distance between 2 blocks
def block2block_angle_dist(self_x, self_y, other_x, other_y, direction, map_size):

    #Determine shortest distance between blocks
    right_move = other_x - self_x if other_x >= self_x else map_size + other_x - self_x - 1
    up_move = other_y - self_y if other_y >= self_y else map_size + other_y - self_y - 1
    left_move = self_x - other_x if self_x >= other_x else map_size + self_x - other_x - 1
    down_move = self_y - other_y if self_y >= other_y else map_size + self_y - other_y - 1

    #Detemine direction of shortest distance
    h_direction = (1, right_move) if right_move < left_move else (-1, left_move)
    v_direction = (1, up_move) if up_move < down_move else (-1, down_move)

    #Calculate angle
    angle = math.atan2(h_direction[0]*h_direction[1], v_direction[0]*v_direction[1])

    #Determine angle relative to current direction
    if direction == 1:
        if angle <= 0:
            angle = math.pi + angle
        else:
            angle = -1*math.pi + angle
    elif direction == 2:
        if angle > 0.5*math.pi:
            angle = -1.5*math.pi + angle
        else:
            angle = angle + 0.5*math.pi
    elif direction == 3:
        if angle < -0.5*math.pi:
            angle = 1.5*math.pi + angle
        else:
            angle = angle - 0.5*math.pi
    
    #Calculate distance
    distance = ((h_direction[1]**2) + (v_direction[1]**2))**0.5

    #Maximum distance and angle values to normalize output between 0 and 1
    max_distance = (((0.5*map_size)**2) + ((0.5*map_size)**2))**0.5
    max_angle = math.pi

    return (angle/max_angle, distance/max_distance)

#Function to determine global direction based on relative direction
def turn2direction(turn, direction):
    #Determine global direction based on current direction
    if direction == 0:
        if turn == 0:
            return 0
        elif turn == 1:
            return 2
        else:
            return 3
    elif direction == 1:
        if turn == 0:
            return 1
        elif turn == 1:
            return 3
        else:
            return 2
    elif direction == 2:
        if turn == 0:
            return 2
        elif turn == 1:
            return 1
        else:
            return 0
    else:
        if turn == 0:
            return 3
        elif turn == 1:
            return 0
        else:
            return 1

#Class to formulate next move based on genetic algorithm
class GenAI(BaseAI):
    #Function to get next move
    def getMove(self, state, w_prey, w_hunter):
        #Case: prey. set parameters
        if state.turn == Config.PREY_TURN:
            self_x = state.prey.head().x
            self_y = state.prey.head().y
            self_dir = state.prey.dir
            food_x = state.food.x
            food_y = state.food.y
            other_x = state.hunter.head().x
            other_y = state.hunter.head().y
            weight = w_prey
        #Case: hunter. set parameters
        else:
            self_x = state.hunter.head().x
            self_y = state.hunter.head().y
            self_dir = state.hunter.dir
            food_x = state.food.x
            food_y = state.food.y
            other_x = state.prey.head().x
            other_y = state.prey.head().y
            weight = w_hunter

        #Determine adjacent blocks
        adjacent_direction_blocks = direction_blocks(self_x, self_y, self_dir, Config.mapSize)

        #Determine status (blocked vs empty) of adjacent blocks
        front_block_status = state.is_empty(Block(adjacent_direction_blocks[0][0], adjacent_direction_blocks[0][1]))
        left_block_status = state.is_empty(Block(adjacent_direction_blocks[1][0], adjacent_direction_blocks[1][1]))
        right_block_status = state.is_empty(Block(adjacent_direction_blocks[2][0], adjacent_direction_blocks[2][1]))

        #print(front_block_status, left_block_status, right_block_status)

        #Determine vector to food and other snake
        food_vector = block2block_angle_dist(self_x, self_y, food_x, food_y, self_dir, Config.mapSize)
        other_snake_vector = block2block_angle_dist(self_x, self_y, other_x, other_y, self_dir, Config.mapSize)

        #Determine distance and angle to food and other snake
        food_angle = food_vector[0]
        food_distance = food_vector[1]
        other_snake_angle = other_snake_vector[0]
        other_snake_distance = other_snake_vector[1]

        #Predict next move based on neural network feedforwarding
        predicted_move = nn.forward_propagation(np.array([front_block_status, left_block_status, right_block_status, self_dir/3, food_angle, food_distance, other_snake_angle, other_snake_distance]), weight)

        #Convert predicted move to global direction
        predicted_direction = turn2direction(predicted_move, self_dir)

        #Determine number of available moves
        available_moves = state.get_available_moves()
        available_moves_list = []
        for i in range(len(available_moves)):
            available_moves_list.append(available_moves[i][0])

        #Avoid collision if possible
        if state.next_state(predicted_direction).is_final():
             for i in range(len(available_moves_list)):
                if not state.next_state(available_moves_list[i]).is_final():
                     predicted_direction = available_moves_list[i]

        return predicted_direction

#Instance of GenAI class to initiate object
genAI = GenAI()
