# the prey's choice in move using expectiminimax.
import random
from BaseAI import BaseAI
from State import State

# a singleton class for the prey ai.
class EMMPreyAI(BaseAI):
    def getMove(self, state):
        available_moves = state.get_available_moves()
        if len(available_moves):
            # gets the next move by randoming selecting from available moves.
            choice = available_moves[random.randint(0, len(available_moves) - 1)]
            next_move = choice[0]
            return next_move
        else:
            return None

# this is used as the singleton instance.
emmPreyAI = EMMPreyAI()