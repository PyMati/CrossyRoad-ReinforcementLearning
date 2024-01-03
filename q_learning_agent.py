from copy import deepcopy
import json
from player import Player
from gameboard import Gameboard
import random
from consts import X_CHUNK_SIZE, Y_CHUNK_SIZE


class QLearningAgent:
    def __init__(self, gameboard: Gameboard, player: Player, train: bool):
        self.is_training = train

        self.player = player
        self.gameboard = gameboard

        self.counter = 0

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.3

        self.episodes = 0

        if not train:
            self.turn_off_learning()

        self.q_values = {}

        self.init_q_table = False
        self.__read_q_values()

        self.states = []
        self.vals = {}

        if self.init_q_table:
            self.__init_vals()
            self.__save_q_table()

        print(f"Settings: {self.alpha} {self.gamma} {self.epsilon}")

    def __init_vals(self):
        for x in range(X_CHUNK_SIZE):
            for y in range(Y_CHUNK_SIZE):
                self.states.append([y, x])

        for state in self.states:
            self.vals[str(state)] = {}
            self.q_values[str(state)] = {}

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

                self.q_values[str(state)][action] = 0

    def __read_q_values(self):
        try:
            with open("q_values.json", "r") as q_table_file:
                saved_vals = q_table_file.read()
                self.q_values = json.loads(saved_vals)
        except FileNotFoundError:
            self.init_q_table = True

    def __save_q_table(self):
        with open("q_values.json", "w") as q_table_file:
            json.dump(self.q_values, q_table_file)

    def get_best_action(self, state):
        max_val = max(list(self.q_values[str(state)].values()))

        max_val_actions = []

        for k, v in self.q_values[str(state)].items():
            if v == max_val:
                max_val_actions.append(k)

        return random.choice(max_val_actions)

    def get_action(self, state):
        possible_actions = list(self.q_values[str(state)].keys())

        random_action = random.choice(possible_actions)
        best_action = self.get_best_action(state)

        if self.epsilon > random.random():
            return random_action
        else:
            return best_action

    def take_action(self):
        if self.player.is_dead or self.player.has_won:
            self.episodes += 1
            print(
                f"Reset Dead:{self.player.is_dead} Win:{self.player.has_won} Episode: {self.episodes}"
            )
            self.player.reset_pos()

        action = self.get_action(self.player.get_player_pos())

        state = self.player.get_player_pos()
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

        reward = (
            self.gameboard.get_reward(next_state) if not self.player.has_won else 100
        )
        if self.is_training:
            self.update(reward, next_state)

    def update(self, reward, next_state):
        current_state = str(self.player.get_player_pos())
        action = self.get_action(current_state)

        current_q_value = self.q_values[current_state][action]
        max_next_q_value = max(list(self.q_values[str(next_state)].values()))
        new_q_value = current_q_value + self.alpha * (
            reward + self.gamma * max_next_q_value - current_q_value
        )

        self.q_values[current_state][action] = new_q_value

        self.__save_q_table()

    def turn_off_learning(self):
        self.alpha = 0
        self.gamma = 0
        self.epsilon = 0
