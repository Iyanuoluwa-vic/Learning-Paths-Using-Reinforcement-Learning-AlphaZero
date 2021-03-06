"""
    This module is to be an implementation for the regular q learning function
    as well as the SARSA q learning function

"""
from manager import get_current_state
from world import *
from agent import *
from location import *
from qtable import *


#   Right now these are just filled with placeholders

def q_learning(world, agent, qtable, action, next_action, learning_rate,
               discount_rate, state_space='big'):
    # this is a pickup or dropoff.. just return because we don't update the q
    # value for it
    if isinstance(qtable[get_current_state(world, agent,
                                           state_space=state_space)], str):
        return

    else:
        state = get_current_state(world, agent, state_space=state_space)
        assert action in ['north', 'south', 'east', 'west']
        next_state = get_current_state(world, agent.pretend_move(action),
                                       state_space=state_space)
        x, y = next_state[:2]
        neighbors = world.get_neighbors(x, y)
        dir = max(get_max_neighbors(neighbors, state, qtable))
        r = world.get_reward(*agent.get_position(), agent.is_holding_block())
        qtable[state][action] = (1 - learning_rate) * qtable[state][action] + (r + discount_rate * qtable[next_state][dir])

def SARSA(world, agent, qtable, action, next_action, learning_rate,
          discount_rate, state_space='big'):
    # this is a pickup or dropoff.. just return because we don't update the q
    # value for it
    if isinstance(qtable[get_current_state(world, agent, state_space=state_space)], str):
        return

    else:
        assert action in ['north', 'south', 'east', 'west']
        assert next_action in ['north', 'south', 'east', 'west']
        state = get_current_state(world, agent, state_space=state_space)
        next_state = get_current_state(world, agent.pretend_move(action),
                                       state_space=state_space)
        r = world.get_reward(*agent.get_position(), agent.is_holding_block())
        qtable[state][action] = qtable[state][action] + learning_rate * ( r + qtable[next_state][next_action] - qtable[state][action])
