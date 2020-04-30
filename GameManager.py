import random
import Config
from Displayer import mainDisplay
from Block import Block
from Snake import Snake
from State import State

from EMMPreyAI import emmPreyAI
from EMMHunterAI import emmHunterAI

from GenPreyAI import genPreyAI
from GenHunterAI import genHunterAI

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT",
    None: "NONE" # For error logging
}

class GameManager:
    def __init__(self):
        # whether or not the game is over.
        self.gameOver = False

        # initializes the first state of the game.
        prey_x = random.randint(0, Config.mapSize - 1)
        prey_y = random.randint(0, Config.mapSize - 1)
        preyHead = Block(prey_x, prey_y)

        hunter_x = (prey_x + Config.mapSize // 2) % Config.mapSize
        hunter_y = (prey_y + Config.mapSize // 2) % Config.mapSize
        hunterHead = Block(hunter_x, hunter_y)

        self.state = State(Config.PREY_TURN, Snake("prey", [preyHead]), Snake("hunter", [hunterHead]))

    def start(self):
        mainDisplay.create_window()

        mainDisplay.draw(self.state)

        turn_counter = 0
        while not self.gameOver:
            # ends the game when the window is closed or a final state is met.
            if mainDisplay.is_closed() or self.state.is_final():
                self.game_over()
                break

            if Config.aiMode == Config.EXPECTIMINIMAX:
                self.expectiminimaxApproach()
            else:
                self.geneticAlgorithmApproach()

            # draws the current state after both players made their turn.
            turn_counter += 1
            if turn_counter % 2 == 0:
                mainDisplay.draw(self.state)
        mainDisplay.draw(self.state)
        

    def expectiminimaxApproach(self):
        nextState = None
        if self.state.turn == Config.PREY_TURN:
            nextState = emmPreyAI.getMove(self.state)
        else:
            nextState = emmHunterAI.getMove(self.state)
        if nextState:
            self.state = nextState

    def geneticAlgorithmApproach(self):
        pass

    def game_over(self):
        self.gameOver = True

# starts the game.
game = GameManager()
game.start()