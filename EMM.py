import random
import Config
from State import State
from Block import Block

def random_choice(state):
        moves = state.get_available_moves()
        if len(moves) == 0:
            return None
        else:
            return moves[random.randint(0, len(moves)-1)][0]

def expectiminimax(decision, max_turn, iter = 1):
        state = decision[1]

        if iter > 3:
            if max_turn == Config.PREY_TURN:
                return decision[0], prey_evaluate(state)
            elif max_turn == Config.HUNTER_TURN:
                return decision[0], hunter_evaluate(state)

        elif not state.has_fruit(): # chance node
            if state.get_available_spaces() == 0:
                if max_turn == Config.PREY_TURN:
                    return decision[0], prey_evaluate(state)
                elif max_turn == Config.HUNTER_TURN:
                    return decision[0], hunter_evaluate(state)

            total = 0
            for space in state.get_available_spaces():
                x = space[0]
                y = space[1]
                next_decision = decision[0], State(state.turn, state.prey.clone(), state.hunter.clone(), False, Block(x, y))
                score = expectiminimax(next_decision, max_turn, iter + 1)[1]
                total += score
            return decision[0], total/len(state.get_available_spaces())

        elif state.turn == max_turn:
            moveset = state.get_available_moves()
            if len(moveset) == 0:
                if max_turn == Config.PREY_TURN:
                    return decision[0], prey_evaluate(state)
                elif max_turn == Config.HUNTER_TURN:
                    return decision[0], hunter_evaluate(state)

            else:
                maxMove = None
                maxUtility = -1000000
                for i in range(0, len(moveset)):
                    child, utility = expectiminimax(moveset[i], max_turn, iter + 1)
                    if utility > maxUtility:
                        maxMove = moveset[i][0]
                        maxUtility = utility
                return maxMove, maxUtility

        elif state.turn != max_turn:
            moveset = state.get_available_moves()
            if len(moveset) == 0:
                if max_turn == Config.PREY_TURN:
                    return decision[0], prey_evaluate(state)
                elif max_turn == Config.HUNTER_TURN:
                    return decision[0], hunter_evaluate(state)

            else:
                minMove = None
                minUtility = 1000000
                for i in range(0, len(moveset)):
                    child, utility = expectiminimax(moveset[i], max_turn, iter + 1)
                    if utility < minUtility:
                        minMove = moveset[i][0]
                        minUtility = utility
                return minMove, minUtility

def prey_evaluate(state):
    # prevent collision
    h1 = 0
    if not state.is_final():
        h1 = 1

    # maximize its size
    h2 = len(state.prey.body)/Config.mapSize

    # minimize prey's distance from fruit
    h3 = 1 - state.distance(state.prey.head(), state.food)/Config.mapSize
    if state.eater == state.prey:
        h3 = 1
    
    # maximizes hunter's distance from fruit
    h4 = state.distance(state.food, state.hunter.head())/Config.mapSize

    # maximize prey's head distance from hunter
    h5 = state.distance(state.prey.head(), state.hunter.head())/Config.mapSize

    w1 = 0.15
    w2 = 0.45
    w3 = 0.20
    w4 = 0.10
    w5 = 0.10
    return h1*w1 + h2*w2 + h3*w3 - h4*w4 + h5*w5

def hunter_evaluate(state):
    # enforce collision
    h1 = 0
    if state.is_final():
        h1 = 1

    # maximize prey's distance from fruit
    h2 = state.distance(state.prey.head(), state.food)/Config.mapSize
    
    # takeaway penalty of hunter's distance from fruit
    h3 = 1
    hunter_fruit_dist = state.distance(state.food, state.hunter.head())
    if hunter_fruit_dist >= Config.hunterPenaltyRadius + 1:
        h3 = 1
    else:
        h3 = hunter_fruit_dist/(Config.hunterPenaltyRadius + 1)

    # minimize prey's tail distance from hunter
    h4 = state.distance(state.prey.tail(), state.hunter.head())/Config.mapSize

    w1 = 0.05
    w2 = 0.05
    w3 = 0.75
    w4 = 0.15
    return h1*w1 + h2*w2 + h3*w3 - h4*w4