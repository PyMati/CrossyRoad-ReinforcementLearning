from copy import deepcopy
from player import Player
from gameboard import Gameboard
import random
from consts import X_CHUNK_SIZE, Y_CHUNK_SIZE


class QLearningAgent:
    def __init__(self, gameboard: Gameboard, player: Player) -> None:
        self.player = player
        self.gameboard = gameboard

        self.counter = 0

        self.alpha = 0.1
        self.gamma = 0.9

        self.states = []
        self.stategy = {}
        self.vals = {}

    def __init_vals(self):
        for x in range(X_CHUNK_SIZE):
            for y in range(Y_CHUNK_SIZE):
                self.states.append([y, x])
                self.strategy[str([y, x])] = random.choice(
                    self.gameboard.get_possible_actions(y, x)
                )

        for state in self.states:
            self.vals[str(state)] = {}
            actions = self.gameboard.get_possible_actions(state[0], state[1])
            for action in actions:
                self.vals[str(state)][action] = {}
                next_state = deepcopy(state)
                if action == "u":
                    next_state[0] -= 1
                elif action == "r":
                    next_state[1] += 1
                elif action == "l":
                    next_state[1] -= 1
                elif action == "d":
                    next_state[0] += 1
                else:
                    pass
                self.vals[str(state)][action][
                    str(next_state)
                ] = self.gameboard.get_reward(next_state)
