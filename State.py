import random
import Config
from Block import Block
from Snake import Snake

class State:
    def __init__(self, turn, preySnake, hunterSnake, foodBlock = None):
        # turn determines who turn it for the next move.
        self.turn = turn

        # creates the two snakes with their respective blocks.
        self.prey   = preySnake
        self.hunter = hunterSnake

        # sets the position for the block.
        self.food   = foodBlock

        # generates a 2-dimensional array for the map with values initialized to 0. 1 for food. 2 for prey. 3 for hunter.
        self.map = [[0] * Config.mapSize for i in range(Config.mapSize)]

        if foodBlock:
            self.map[foodBlock.x][foodBlock.y] = 1

        for block in self.prey.body:
            if self.map[block.x][block.y] == 0:
                self.map[block.x][block.y] = 2
            else:
                self.map[block.x][block.y] = 4
        
        for block in self.hunter.body:
            if self.map[block.x][block.y] == 0:
                self.map[block.x][block.y] = 3
            else:
                self.map[block.x][block.y] = 4

        # stores the available spaces on the map.
        self.availableSpaces = []
    
        for i in range(0, Config.mapSize):
            for j in range(0, Config.mapSize):
                if self.map[i][j] == 0:
                    self.availableSpaces.append([i, j])
        
        # if there is no food, tries to add a food in a random spot.
        if self.food is None and len(self.availableSpaces):
            space = self.availableSpaces[random.randint(0, len(self.availableSpaces) - 1)]
            self.food = Block(space[0], space[1])
            self.map[self.food.x][self.food.y] = 1
    
    def is_final(self):
        if self.food is None:
            return True
        
        for i in range(0, Config.mapSize):
            for j in range(0, Config.mapSize):
                if self.map[i][j] == 4:
                    return True

    def can_move(self, move, snake):
        if len(snake.body) >= 2 and ((move == 0 and snake.dir == 1) or (move == 1 and snake.dir == 0) or (move == 2 and snake.dir == 3) or (move == 3 and snake.dir == 2)):
            return False
        return True

    def getAvailableSpaces(self):
        return self.availableSpaces

    

    def getAvailableMoves(self):
        available_moves = []
        for move in range(0, 4):
            if self.turn == Config.PREY_TURN:
                if not self.can_move(move, self.prey):
                    continue
                nextTurn = Config.HUNTER_TURN
                nextPrey = Snake("prey", self.prey.cloneBlocks(), move)
                nextHunter = Snake("hunter", self.hunter.cloneBlocks(), self.hunter.dir)
                movingSnake = nextPrey
            else:
                if not self.can_move(move, self.hunter):
                    continue
                nextTurn = Config.PREY_TURN
                nextPrey = Snake("prey", self.prey.cloneBlocks(), self.prey.dir)
                nextHunter = Snake("hunter", self.hunter.cloneBlocks(), move)
                movingSnake = nextHunter
            
            nextBlock = movingSnake.next_move()

            movingSnake.addHead(nextBlock)
            if self.food and self.food.x == nextBlock.x and self.food.y == nextBlock.y:
                available_moves.append([move, State(nextTurn, nextPrey, nextHunter)])
            else:
                movingSnake.removeTail()
                if self.food is None:
                    available_moves.append([move, State(nextTurn, nextPrey, nextHunter)])
                else:
                    available_moves.append([move, State(nextTurn, nextPrey, nextHunter, self.food.clone())])
            
        return available_moves


