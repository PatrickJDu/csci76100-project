# the prey's choice in move using expectiminimax.
import random
import Config
import EMM
from BaseAI import BaseAI

# a singleton class for the prey ai.
class EMMPreyAI(BaseAI):
    def getMove(self, state):
        decision = None, state
        choice = EMM.expectiminimax(decision, Config.PREY_TURN)[0]
        return choice

# this is used as the singleton instance.
emmPreyAI = EMMPreyAI()