import random
from BaseAI import BaseAI
from State import State

class EMMHunterAI(BaseAI):
    def getMove(self, state):
        choices = state.getAvailableMoves()
        choice = choices[random.randint(0, len(choices) - 1)]
        next_state = choice[1]
        return next_state

emmHunterAI = EMMHunterAI()