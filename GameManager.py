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
    # handles what the game manager does.
    def __init__(self):
        if Config.aiMode == Config.GENETIC_ALGORITHM:
            self.initGeneticAlgorithm()

        elif Config.aiMode == Config.EXPECTIMINIMAX:
            self.initExpectiminimax()

        # keeps the program alive until game window is closed.
        while Config.showWindow and not mainDisplay.is_closed():
            pass

    # game manager init for genetic algorithm goes here
    def initGeneticAlgorithm(self):
        pass

    # game manager init for expectiminimax algorithm goes here
    def initExpectiminimax(self):
        self.run(1)

    # creates the first state of a run and returns it.
    def getStartState(self):
        # prey starts at a random position with a length of 1.
        prey_x = random.randint(0, Config.mapSize - 1)
        prey_y = random.randint(0, Config.mapSize - 1)
        prey_head = Block(prey_x, prey_y)

        # hunter starts at the opposite position with a length of 1.
        hunter_x = (prey_x + Config.mapSize // 2 + 1) % Config.mapSize
        hunter_y = (prey_y + Config.mapSize // 2 + 1) % Config.mapSize
        hunter_head = Block(hunter_x, hunter_y)

        # builds the first state and adds in the food at a random available position.
        return State(Config.PREY_TURN, Snake("prey", [prey_head]), Snake("hunter", [hunter_head]))

        # Counts how many times the hunter comes within 2 blocks of the fruit
        # WIP

    def hunter_from_fruit(self, state, count):
        # Grab the x and y of both the fruit and the hunter
        fruit_x, fruit_y = state.food.x, state.food.y
        hunter_x, hunter_y = state.hunter.body[0].x, state.hunter.body[0].y
        # Checking here if the hunter is ever 2 blocks within the fruits territory
        x_check = False
        y_check = False
        # from x coordinate for fruit -2 to +2. We do a check to see if hunter's x coordinate is in here
        for i in range(fruit_x - 2, fruit_x + 2):
            if hunter_x == i % Config.mapSize:
                x_check = True
        # same idea as x
        for i in range(fruit_y - 2, fruit_y + 2):
            if hunter_y == i % Config.mapSize:
                y_check = True
        # if both of these are true means that hunter is within 2 block range of the fruit
        if y_check and x_check:
            count += 1
        print(count)
        return count

    # run the game n number of times then returns a list of scores of each final state.
    def run(self, numIterations = 1):
        scores = []
        count = 0
        # runs the game n iterations.
        for _ in range(0, numIterations):
            # creates a new start state and begins the game for the iteration. 
            state = self.getStartState()

            turn_counter = 0
            while not state.is_final():
                # draws the state of the game after both players made their turn.
                if Config.showWindow and turn_counter % 2 == 0 and not mainDisplay.is_closed():
                    mainDisplay.draw(state)
                count = self.hunter_from_fruit(state, count)
                turn_counter += 1

                # continues playing until it reach a final state.
                # if a final state is met, the loop continues to keep the game window up.
                if not state.is_final():
                    # decides the next action based on the ai mode.
                    if Config.aiMode == Config.EXPECTIMINIMAX:
                        state = self.expectiminimaxApproach(state)
                    else:
                        state = self.geneticAlgorithmApproach(state)
                
                # To give the functionality of closing the window.
                if Config.showWindow and mainDisplay.is_closed():
                    pass
            
            # draws the last state.
            if Config.showWindow and not mainDisplay.is_closed():
                mainDisplay.draw(state)

            scores.append(state.score())

        return scores, count
                
    # returns the next state based on expectiminimax.
    def expectiminimaxApproach(self, state):
        next_state = None
        if state.turn == Config.PREY_TURN:
            next_state = state.next_state(emmPreyAI.getMove(state))
        else:
            next_state = state.next_state(emmHunterAI.getMove(state))

        if next_state is None:
            return state
        return next_state

    # returns the next state based on genetic algorithm.
    def geneticAlgorithmApproach(self, state):
        next_state = None
        if state.turn == Config.PREY_TURN:
            next_state = state.next_state(genPreyAI.getMove(state))
        else:
            next_state = state.next_state(genHunterAI.getMove(state))

        if next_state is None:
            return state
        return next_state

# starts the game.
game = GameManager()