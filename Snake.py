import Config
from Block import Block

# a snake in the game which is a list of adjacent blocks.
class Snake:
    def __init__(self, name, body = [], dir = 0):
        # the name of the snake, either "prey" or "hunter"
        self.name = name

        # the body of the snake, an array of blocks where body[-1] is the head and body[0] is the tail.
        self.body = body

        # the direction that the snake is moving in.
        # Either UP, DOWN, LEFT, or RIGHT.
        self.dir = dir

    # returns a deep copy of the snake.
    def clone(self):
        return Snake(self.name, self.cloneBlocks(), self.dir)

    # returns a deep copy of the body.
    def cloneBlocks(self):
        trail = []
        for block in self.body:
            trail.append(block.clone())
        return trail

    # returns the head of the snake.
    def head(self):
        return self.body[-1]
    
    # returns the tail of the snake.
    def tail(self):
        return self.body[0]

    # returns the next block position of the snake's head based on its direction.
    def next_move(self):
        if self.dir == Config.UP:
            return Block(self.head().x, (self.head().y + 1) % Config.mapSize)
        elif self.dir == Config.DOWN:
            return Block(self.head().x, (self.head().y - 1) % Config.mapSize)
        elif self.dir == Config.LEFT:
            return Block((self.head().x - 1) % Config.mapSize, self.head().y)
        elif self.dir == Config.RIGHT:
            return Block((self.head().x + 1) % Config.mapSize, self.head().y)

    # adds a block to the head of the snake.
    def addHead(self, block):
        self.body.append(block)

    # removes the tail block of the snake.
    def removeTail(self):
        self.body.remove(self.tail())
