# the hunter's choice in move using expectiminimax.
import random
import Config
import EMM
from BaseAI import BaseAI

# a singleton class for the hunter ai.
class EMMHunterAI(BaseAI):
    def getMove(self, state):
        decision = None, state
        choice = EMM.expectiminimax(decision, Config.HUNTER_TURN)[0]
        return choice

# this is used as the singleton instance.
emmHunterAI = EMMHunterAI()