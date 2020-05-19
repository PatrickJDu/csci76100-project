import random
import Config
from Block import Block
from Snake import Snake

# the state of the game. holds the current turn. prey and hunter snake info.
class State:
    # set withFruit to false to supply the next states without the fruit placed on the map.
    def __init__(self, turn, preySnake, hunterSnake, withFruit = True, foodBlock = None, eater = None):
        # turn determines who turn it for the next move.
        self.turn = turn

        # creates the two snakes with their respective blocks.
        self.prey   = preySnake
        self.hunter = hunterSnake

        # the snake that ate the previous fruit in the previous state
        self.eater = eater

        # represents the block for the food.
        self.food = foodBlock

        # generates a 2-dimensional array for the map with values initialized to 0. 1 for food. 2 for prey. 3 for hunter.
        self.map = [[Config.EMPTY_BLOCK] * Config.mapSize for i in range(Config.mapSize)]

        # whether or not this is the final state
        self.final = None
        
        # sets the fruit block on the map.
        if self.food:
            self.map[self.food.x][self.food.y] = Config.FRUIT_BLOCK

        # sets the prey blocks on the map.
        for block in self.prey.body:
            if self.map[block.x][block.y] == Config.EMPTY_BLOCK:
                self.map[block.x][block.y] = Config.PREY_BLOCK
            else:
                if self.map[block.x][block.y] == Config.PREY_BLOCK:
                    self.set_final_state(Config.PREY_CAUGHT_SELF)
                elif self.map[block.x][block.y] == Config.HUNTER_BLOCK:
                    self.set_final_state(Config.PREY_CAUGHT_HUNTER)

                # if a collision is detected, the block is treated as a fail block and the state becomes a final state.
                self.map[block.x][block.y] = Config.COLLISION_BLOCK
        
        # sets the hunter blocks on the map.
        for block in self.hunter.body:
            if self.map[block.x][block.y] == Config.EMPTY_BLOCK:
                self.map[block.x][block.y] = Config.HUNTER_BLOCK
            else:
                if self.map[block.x][block.y] == Config.PREY_BLOCK:
                    self.set_final_state(Config.HUNTER_CAUGHT_PREY)
                elif self.map[block.x][block.y] == Config.HUNTER_BLOCK:
                    self.set_final_state(Config.HUNTER_CAUGHT_SELF)

                # if a collision is detected, the block is treated as a fail block and the state becomes a final state.
                self.map[block.x][block.y] = Config.COLLISION_BLOCK

        # stores the available spaces on the map.
        self.available_spaces = []
    
        for i in range(0, Config.mapSize):
            for j in range(0, Config.mapSize):
                if self.map[i][j] == Config.EMPTY_BLOCK:
                    self.available_spaces.append([i, j])
        
        # if there is no food, tries to add a food in a random spot.
        if self.food is None and len(self.available_spaces) and withFruit:
            space = self.available_spaces[random.randint(0, len(self.available_spaces) - 1)]
            self.food = Block(space[0], space[1])
            self.map[self.food.x][self.food.y] = Config.FRUIT_BLOCK

        # if no more food can be spawned, the state becomes a final state.
        if self.food is None and len(self.available_spaces) == 0:
            self.set_final_state(Config.BOARD_FULL)

    # sets the final state once
    def set_final_state(self, final_state):
        if self.final is None:
            self.final = final_state

    # returns true if the state is in a final state.
    def is_final(self):
        return self.final is not None

    # returns the type of final state
    def get_final_state(self):
        return self.final

    # returns true if the given position of the block is empty.
    def is_empty(self, block):
        return self.map[block.x][block.y] == Config.EMPTY_BLOCK

    def score(self):
        return len(self.prey.body) - 1

    # returns true if there is a fruit block on the map.
    def has_fruit(self):
        return self.food is not None

    # returns the shortest distance between two blocks for no walls.
    def distance(self, block1, block2):
         # returns a value that is reflected from the cetner of the map.
        def reflectFromCenter(value):
            if value < Config.mapCenter1:
                return Config.mapCenter1 - 1 - value
            else:
                return Config.mapCenter1 + Config.mapCenter2 - 1 - (value - Config.mapCenter1)
        
        if block1 is None or block2 is None:
            return 0

        x_dist = min(abs(block1.x - block2.x), abs(reflectFromCenter(block1.x) - reflectFromCenter(block2.x)))
        y_dist = min(abs(block1.y - block2.y), abs(reflectFromCenter(block1.y) - reflectFromCenter(block2.y)))
        return x_dist + y_dist

    # returns the available spaces in the state.
    def get_available_spaces(self):
        return self.available_spaces

    # returns the available moves in the state based on the turn.
    # set withFruit to false to supply the next states without the fruit placed on the map.
    def get_available_moves(self, withFruit = True):
        available_moves = []

        if self.is_final():
            return available_moves

        up_state    = self.next_state(Config.UP, withFruit)
        down_state  = self.next_state(Config.DOWN, withFruit)
        left_state  = self.next_state(Config.LEFT, withFruit)
        right_state = self.next_state(Config.RIGHT, withFruit)

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
        if len(snake.body) >= 2:
            # prevents a snake of at least length 2 from moving in its opposite direction.
            if move == Config.UP and snake.dir == Config.DOWN:
                return False
            if move == Config.DOWN and snake.dir == Config.UP:
                return False
            if move == Config.LEFT and snake.dir == Config.RIGHT:
                return False
            if move == Config.RIGHT and snake.dir == Config.LEFT:
                return False

        head = snake.head()
        if snake.name == "hunter" and self.distance(head, self.food) == 1:
            # prevents hunter from eating the fruit
            if move == Config.UP and (head.y+1) % Config.mapSize == self.food.y:
                return False
            if move == Config.DOWN and (head.y-1) % Config.mapSize == self.food.y:
                return False
            if move == Config.LEFT and (head.x-1) % Config.mapSize == self.food.x:
                return False
            if move == Config.RIGHT and (head.x+1) % Config.mapSize == self.food.x:
                return False

        return True

    # returns the a copy of the hunter's body with a size that is (prey's size // 5 + 1)
    def hunter_growth(self):
        hunter_blocks = self.hunter.cloneBlocks()
        while len(hunter_blocks) < len(self.prey.body) // 5 + 1:
            tail = hunter_blocks[0].clone()
            hunter_blocks.insert(0, tail)
        return hunter_blocks

    # returns the next state that the game will be in based on the move.
    # set withFruit to false to supply the next states without the fruit placed on the map.
    def next_state(self, move, withFruit = True):
        if move is not None:
            moving_snake = None
            if self.turn is Config.PREY_TURN:
                if self.can_move(move, self.prey):
                    next_turn = Config.HUNTER_TURN
                    next_prey = Snake("prey", self.prey.cloneBlocks(), move)
                    next_hunter = Snake("hunter", self.hunter.cloneBlocks(), self.hunter.dir)
                    moving_snake = next_prey
            elif self.turn is Config.HUNTER_TURN:
                if self.can_move(move, self.hunter):
                    next_turn = Config.PREY_TURN
                    next_prey = Snake("prey", self.prey.cloneBlocks(), self.prey.dir)
                    next_hunter = Snake("hunter", self.hunter.cloneBlocks(), move)
                    moving_snake = next_hunter
            
            if moving_snake:
                next_block = moving_snake.next_move()
                moving_snake.addHead(next_block)
                if self.food and self.food.x == next_block.x and self.food.y == next_block.y:
                    return State(next_turn, next_prey, next_hunter, withFruit, eater = moving_snake)
                else:
                    moving_snake.removeTail()
                    if self.food is None:
                        return State(next_turn, next_prey, next_hunter, withFruit)
                    else:
                        return State(next_turn, next_prey, next_hunter, withFruit, self.food.clone())
        return None
