from copy import deepcopy
import random
from tempfile import tempdir
from player import Player
from gameboard import Gameboard
from consts import X_CHUNK_SIZE, Y_CHUNK_SIZE
import numpy as np
import json


class ApproximationAgent:
    def __init__(self, gameboard: Gameboard, player: Player, train: bool):
        # Needed objects
        self.player = player
        self.gameboard = gameboard

        # Training aprams
        self.is_training = train
        self.are_weights_loaded = True

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.3

        self.features_num = 7
        self.__load_weights()

        if not self.are_weights_loaded:
            self.__init_weights()

        self.numbers_actions_classes = {
            0: "u",
            1: "d",
            2: "l",
            3: "r",
            4: "s",
        }

        self.actions_numbers_classes = {
            "u": 0,
            "d": 1,
            "l": 2,
            "r": 3,
            "s": 4,
        }

        self.actions_next_pos = {
            "u": [-1, 0],
            "d": [1, 0],
            "l": [0, -1],
            "r": [0, 1],
            "s": [0, 0],
        }

        self.counter = 0

        self.car_positions = self.gameboard.static_cars_pos

        self.states = []
        self.possible_actions = {}

        self.prv_state: Gameboard = None
        self.prv_action = None

        self.__init_vals()

    def __init_vals(self):
        for x in range(X_CHUNK_SIZE):
            for y in range(Y_CHUNK_SIZE):
                self.states.append([y, x])

        for state in self.states:
            self.possible_actions[str(state)] = self.gameboard.get_possible_actions(
                state[0], state[1]
            )
            self.possible_actions[str(state)].remove("s")

    def __load_weights(self):
        try:
            with open("wh.json", "r") as file:
                self.weights = np.array(json.load(file)["w"])
        except FileNotFoundError:
            self.are_weights_loaded = False

    def __init_weights(self):
        self.weights = np.random.rand(self.features_num)
        with open("wh.json", "w") as file:
            json.dump({"w": self.weights.tolist()}, file)

    def __save_weigths(self):
        with open("wh.json", "w") as file:
            json.dump({"w": self.weights.tolist()}, file)

    def approximate(self, features):
        return np.dot(self.weights.astype(np.float64), features.astype(np.float64))

    def prepare_features(self, player_pos, action):
        features = []

        features += [
            player_pos[0] - self.gameboard.end_x_pos,
            player_pos[1] - self.gameboard.y_chunk_multiplier - 1,
        ]

        add_zero = True
        move = np.array(self.actions_next_pos[action])
        player_np_pos = np.array(player_pos)
        next_pos = list(player_np_pos + move)
        for car in self.car_positions:
            if next_pos == car:
                features.append(1)
                add_zero = False
        if add_zero:
            features.append(0)

        features += [
            next_pos[0] - self.gameboard.end_x_pos,
            next_pos[1] - self.gameboard.y_chunk_multiplier - 1,
        ]

        features.append(1) if next_pos[
            0
        ] == self.gameboard.y_chunk_multiplier - 1 else features.append(0)
        features.append(1) if next_pos[
            1
        ] == self.gameboard.end_x_pos else features.append(0)

        features = np.array(features)

        return features

    def update(self, reward, state, next_state, action, terminal=1):
        if terminal == 1:
            next_state_features = self.prepare_features(
                next_state.players[0].get_player_pos(), self.get_best_action(next_state)
            )
            next_state_approxim = self.approximate(next_state_features) * terminal

            multiplier = self.prepare_features(
                next_state.players[0].get_player_pos(), action
            )
        else:
            next_state_approxim = 0

            multiplier = 1

        state_features = self.prepare_features(
            state.players[0].get_player_pos(), action
        )
        state_approxim = self.approximate(state_features)

        delta = reward + self.gamma * next_state_approxim - state_approxim

        # print(delta, terminal)

        self.weights += self.alpha * delta * multiplier

        self.__save_weigths()

    def get_best_action(self, state):
        current_player_pos = state.players[0].get_player_pos()
        possible_actions = self.possible_actions[str(current_player_pos)]

        action_val_dict = {}
        for action in possible_actions:
            if action == "s":
                continue
            features = self.prepare_features(current_player_pos, action)
            action_val_dict[action] = self.approximate(features)

        best_value = max(action_val_dict.values())
        best_actions = [
            action for action, value in action_val_dict.items() if value == best_value
        ]
        best_action = random.choice(best_actions)
        return best_action

    def get_action(self, state):
        r = np.random.random()
        if r < self.epsilon:
            return random.choice(
                self.possible_actions[str(self.player.get_player_pos())]
            )

        return self.get_best_action(state)

    def final_action(self, action):
        if action == "r":
            self.player.go_right()
        elif action == "l":
            self.player.go_left()
        elif action == "u":
            self.player.go_up()
        elif action == "d":
            self.player.go_down()
        else:
            self.player.stay()

    def take_action(self):
        if self.counter == 10:
            self.counter = 0
            if self.is_training:
                reward = 0

                if self.prv_action is None and self.prv_state is None:
                    action = random.choice(
                        self.possible_actions[str(self.player.get_player_pos())]
                    )
                    self.prv_action = action
                    self.prv_state = deepcopy(self.gameboard)
                    player_copy = deepcopy(self.player)
                    self.prv_state.players = [player_copy]
                    self.final_action(action)
                    return

                if self.player.has_won:
                    reward += 10
                    self.update(
                        reward,
                        self.prv_state,
                        self.gameboard,
                        self.prv_action,
                        0,
                    )
                    self.player.reset_pos()
                elif self.player.is_dead:
                    reward -= 10
                    self.update(
                        reward,
                        self.prv_state,
                        self.gameboard,
                        self.prv_action,
                        0,
                    )
                    self.player.reset_pos()
                else:
                    if (
                        self.player.get_player_pos()[0]
                        < self.prv_state.players[0].get_player_pos()[0]
                        or self.player.get_player_pos()[1]
                        < self.prv_state.players[0].get_player_pos()[1]
                    ):
                        reward -= 10  # Penalty for moving backward
                    else:
                        reward += 1

                    self.update(reward, self.prv_state, self.gameboard, self.prv_action)

                action = self.get_action(self.gameboard)
                self.prv_action = action
                self.prv_state = deepcopy(self.gameboard)
                player_copy = deepcopy(self.player)
                self.prv_state.players = [player_copy]
            else:
                action = self.get_best_action(self.gameboard)

            self.final_action(action)

        else:
            self.counter += 1
