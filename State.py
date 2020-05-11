import random
import Config
from Block import Block
from Snake import Snake

# the state of the game. holds the current turn. prey and hunter snake info.
class State:
    def __init__(self, turn, preySnake, hunterSnake, foodBlock = None):
        # turn determines who turn it for the next move.
        self.turn = turn

        # creates the two snakes with their respective blocks.
        self.prey   = preySnake
        self.hunter = hunterSnake

        # sets the position for the block.
        self.food = foodBlock

        # generates a 2-dimensional array for the map with values initialized to 0. 1 for food. 2 for prey. 3 for hunter.
        self.map = [[0] * Config.mapSize for i in range(Config.mapSize)]

        # whether or not this is the final state
        self.final = False

        # if a food block was passed, sets the food block
        if self.food:
            self.map[self.food.x][self.food.y] = 1

        # sets the prey blocks on the map.
        for block in self.prey.body:
            if self.map[block.x][block.y] == 0:
                self.map[block.x][block.y] = 2
            else:
                # if a collision is detected, the block is treated as a fail block and the state becomes a final state.
                self.map[block.x][block.y] = 4
                self.final = True
        
        # sets the hunter blocks on the map.
        for block in self.hunter.body:
            if self.map[block.x][block.y] == 0:
                self.map[block.x][block.y] = 3
            else:
                # if a collision is detected, the block is treated as a fail block and the state becomes a final state.
                self.map[block.x][block.y] = 4
                self.final = True

        # stores the available spaces on the map.
        self.available_spaces = []
    
        for i in range(0, Config.mapSize):
            for j in range(0, Config.mapSize):
                if self.map[i][j] == 0:
                    self.available_spaces.append([i, j])
        
        # if there is no food, tries to add a food in a random spot.
        if self.food is None and len(self.available_spaces):
            space = self.available_spaces[random.randint(0, len(self.available_spaces) - 1)]
            self.food = Block(space[0], space[1])
            self.map[self.food.x][self.food.y] = 1

        # if no more food can be spawned, the state becomes a final state.
        if self.food is None:
            self.final = True

    # returns true if the state is in its final state.
    def is_final(self):
        return self.final

    # returns true if the given position of the block is empty.
    def is_empty(self, block):
        return self.map[block.x][block.y] == 0

    # returns the available spaces in the state.
    def get_available_spaces(self):
        return self.available_spaces

    # returns the available moves in the state based on the turn.
    def get_available_moves(self):
        available_moves = []

        up_state    = self.next_state(Config.UP)
        down_state  = self.next_state(Config.DOWN)
        left_state  = self.next_state(Config.LEFT)
        right_state = self.next_state(Config.RIGHT)

        if up_state:
            available_moves.append([Config.UP, up_state])
        if down_state:
            available_moves.append([Config.DOWN, down_state])
        if left_state:
            available_moves.append([Config.LEFT, left_state])
        if right_state:
            available_moves.append([Config.RIGHT, right_state])
            
        return available_moves

    # returns true if the specifed snake can make the specifed move.
    def can_move(self, move, snake):
        if len(snake.body) >= 2 and ((move == 0 and snake.dir == 1) or (move == 1 and snake.dir == 0) or (move == 2 and snake.dir == 3) or (move == 3 and snake.dir == 2)):
            # prevents a snake of at least length 2 from moving in its opposite direction.
            return False

        return True

    # returns the next state that the game will be in based on the move.
    def next_state(self, move):
        if move is not None:
            moving_snake = None
            if self.turn is Config.PREY_TURN:
                if self.can_move(move, self.prey):
                    next_turn = Config.HUNTER_TURN
                    next_prey = Snake("prey", self.prey.cloneBlocks(), move)
                    next_hunter = Snake("hunter", self.hunter.cloneBlocks(), self.hunter.dir)
                    moving_snake = next_prey
            else:
                if self.can_move(move, self.hunter):
                    next_turn = Config.PREY_TURN
                    next_prey = Snake("prey", self.prey.cloneBlocks(), self.prey.dir)
                    next_hunter = Snake("hunter", self.hunter.cloneBlocks(), move)
                    moving_snake = next_hunter
            
            if moving_snake:
                next_block = moving_snake.next_move()
                moving_snake.addHead(next_block)
                if self.food and self.food.x == next_block.x and self.food.y == next_block.y:
                    return State(next_turn, next_prey, next_hunter)
                else:
                    moving_snake.removeTail()
                    if self.food is None:
                        return State(next_turn, next_prey, next_hunter)
                    else:
                        return State(next_turn, next_prey, next_hunter, self.food.clone())
        return None
