class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def clone(self):
        return Block(self.x, self.y)