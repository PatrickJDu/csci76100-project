import random
import Config
from Displayer import mainDisplay
from Block import Block
from Snake import Snake
from State import State

# Expectiminimax imports
from EMMPreyAI import emmPreyAI
from EMMHunterAI import emmHunterAI

# Genetic Algorithm imports
from GenPreyAI import genPreyAI
from GenHunterAI import genHunterAI

# manages the entire game.
class GameManager:
    def __init__(self):
        # whether or not the game is over.
        self.gameOver = False

        # initializes the first state of the game.
        # prey starts at a random position with a length of 1.
        prey_x = random.randint(0, Config.mapSize - 1)
        prey_y = random.randint(0, Config.mapSize - 1)
        prey_head = Block(prey_x, prey_y)

        # hunter starts at the opposite position with a length of 1.
        hunter_x = (prey_x + Config.mapSize // 2 + 1) % Config.mapSize
        hunter_y = (prey_y + Config.mapSize // 2 + 1) % Config.mapSize
        hunter_head = Block(hunter_x, hunter_y)

        # builds the first state and adds in the food at a random available position.
        self.state = State(Config.PREY_TURN, Snake("prey", [prey_head]), Snake("hunter", [hunter_head]))

    # starts the game.
    def start(self):
        # creates the window.
        mainDisplay.create_window()
        
        # ends the game when the window is closed. 
        turn_counter = 0
        final_state = self.state.is_final()
        while not mainDisplay.is_closed():
            # draws the state of the game after both players made their turn.
            if turn_counter % 2 == 0:
                mainDisplay.draw(self.state)
            
            turn_counter += 1

            # continues playing until it reach a final state.
            # if a final state is met, the loop continues to keep the game window up.
            if not final_state:
                # decides the next action based on the ai mode.
                if Config.aiMode == Config.EXPECTIMINIMAX:
                    self.expectiminimaxApproach()
                else:
                    self.geneticAlgorithmApproach()

                final_state = self.state.is_final()
                
    # returns the next state based on expectiminimax.
    def expectiminimaxApproach(self):
        next_state = None
        if self.state.turn == Config.PREY_TURN:
            next_state = self.state.next_state(emmPreyAI.getMove(self.state))
        else:
            next_state = self.state.next_state(emmHunterAI.getMove(self.state))
        if next_state:
            self.state = next_state

    # returns the next state based on genetic algorithm.
    def geneticAlgorithmApproach(self):
        next_state = None
        if self.state.turn == Config.PREY_TURN:
            next_state = self.state.next_state(genPreyAI.getMove(self.state))
        else:
            next_state = self.state.next_state(genHunterAI.getMove(self.state))
        if next_state:
            self.state = next_state

# starts the game.
game = GameManager()
game.start()