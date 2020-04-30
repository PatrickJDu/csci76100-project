import Config
from Block import Block

directionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

class Snake:
    def __init__(self, name, body = [], dir = 0):
        # the name of the snake, either "prey" or "hunter"
        self.name = name

        # the body of the snake, an array of cube positions where body[-1] is the head and body[0] is the tail.
        self.body = body

        # the direction that the snake is moving in.
        self.dir = dir

    def cloneBlocks(self):
        trail = []
        for block in self.body:
            trail.append(block.clone())
        return trail

    def head(self):
        return self.body[-1]
    
    def tail(self):
        return self.body[0]

    def next_move(self):
        if self.dir == 0: # Move up
            return Block(self.head().x, (self.head().y + 1) % Config.mapSize)
        elif self.dir == 1: # Move down
            return Block(self.head().x, (self.head().y - 1) % Config.mapSize)
        elif self.dir == 2: # Move left
            return Block((self.head().x - 1) % Config.mapSize, self.head().y)
        elif self.dir == 3: # Move right
            return Block((self.head().x + 1) % Config.mapSize, self.head().y)

    def addHead(self, block):
        self.body.append(block)

    def removeTail(self):
        self.body.remove(self.tail())
