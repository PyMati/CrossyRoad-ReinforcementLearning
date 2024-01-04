from copy import deepcopy
from player import Player
from gameboard import Gameboard
import random
from consts import X_CHUNK_SIZE, Y_CHUNK_SIZE


class PassiveLearningAgent:
    def __init__(self, gameboard: Gameboard, player: Player):
        self.player = player
        self.gameboard = gameboard

        self.counter = 0

        self.alpha = 0.1
        self.gamma = 0.9
        self.theta = 0.0001

        self.states = []
        self.strategy = {}
        self.vals = {}
        self.__init_vals()

        self.V = self.strategy_evaluation()
        # print(self.V)
        self.str = self.value_iteration()

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

    def strategy_evaluation(self):
        V = dict()
        V_new = dict()
        for state in self.states:
            V[str(state)] = 0
            V_new[str(state)] = 0

        delta = float("inf")
        while delta > self.theta:
            delta = 0
            for state in self.states:
                policy_eval = 0
                for action in self.gameboard.get_possible_actions(state[0], state[1]):
                    prob = 1 / len(
                        self.gameboard.get_possible_actions(state[0], state[1])
                    )
                    new_eval = 0

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

                    trans_prob = 1 / len(self.vals[str(state)].keys())
                    for _, values in self.vals[str(state)].items():
                        reward = list(values.values())[0]
                        new_eval += trans_prob * (
                            reward + self.gamma * V[str(next_state)]
                        )

                    policy_eval += new_eval * prob

                V_new[str(state)] = policy_eval

            delta = max(
                delta,
                max(abs(V[str(state)] - V_new[str(state)]) for state in self.states),
            )
            V = deepcopy(V_new)

        return V

    def value_iteration(self):
        V = {}
        strategy = {}
        for state in self.states:
            V[str(state)] = 0
            strategy[str(state)] = random.choice(
                self.gameboard.get_possible_actions(state[0], state[1])
            )

        delta = float("inf")
        while delta > self.theta:
            delta = 0

            for state in self.states:
                prv_state = V[str(state)]
                best_action = None
                best_value = float("-inf")

                for action in self.gameboard.get_possible_actions(state[0], state[1]):
                    new_eval = 0

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

                    trans_prob = 1 / len(self.vals[str(state)].keys())
                    for _, values in self.vals[str(state)].items():
                        reward = list(values.values())[0]
                        new_eval += trans_prob * (
                            reward + self.gamma * V[str(next_state)]
                        )

                    if new_eval > best_value:
                        best_action = action
                        best_value = new_eval

                V[str(state)] = best_value
                strategy[str(state)] = best_action

                delta = max(delta, abs(prv_state - V[str(state)]))

        return strategy

    def take_action(self):
        if self.counter >= 10:
            self.counter = 0
            action = self.str[str(self.player.get_player_pos())]
            if action == "u":
                self.player.go_up()
            elif action == "r":
                self.player.go_right()
            elif action == "l":
                self.player.go_left()
            elif action == "d":
                self.player.go_down()
            else:
                pass
        else:
            self.counter += 1
