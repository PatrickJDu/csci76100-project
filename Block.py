# a single block on the map.
class Block:
    # initializes a block on the map at position (x, y).
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    
    # returns a newly created block with the same (x, y) position as the instance.
    def clone(self):
        return Block(self.x, self.y)