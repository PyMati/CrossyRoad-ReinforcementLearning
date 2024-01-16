from copy import deepcopy
import random
import stat
from tracemalloc import is_tracing

from matplotlib.pylab import rand
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
        self.epsilon = 0.5

        self.features_num = 11
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

        self.all_possible_car_states = 9
        self.possible_cars_pos = []
        self.reward_maps = {}

        self.__init_all_car_states()

        self.counter = 0

        self.states = []
        self.possible_actions = {}

        self.prv_state = []

        self.__init_vals()

    def __init_all_car_states(self):
        gameboard_copy = deepcopy(self.gameboard)
        while len(self.possible_cars_pos) != self.all_possible_car_states:
            pos = gameboard_copy.get_cars_pos()
            if pos in self.possible_cars_pos:
                pass
            else:
                self.possible_cars_pos.append(pos)
                self.reward_maps[str(pos)] = gameboard_copy.reward_map.copy()

            gameboard_copy.init_cars()
            gameboard_copy.move_cars()
            gameboard_copy.update_reward_map()

    def __init_vals(self):
        for x in range(X_CHUNK_SIZE):
            for y in range(Y_CHUNK_SIZE):
                self.states.append([y, x])

        for car_states in self.possible_cars_pos:
            self.possible_actions[str(car_states)] = {}
            for state in self.states:
                self.possible_actions[str(car_states)][
                    str(state)
                ] = self.gameboard.get_possible_actions(state[0], state[1])

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

    def __prepare_features(self, player_pos, cars_pos):
        features = [*player_pos]

        car_counter = 0
        for pos in cars_pos:
            features.append(pos[0])
            features.append(pos[1])
            car_counter += 1

        while car_counter != 4:
            features.append(-5)
            features.append(-5)
            car_counter += 1

        distance_to_end = np.sqrt(
            (player_pos[0] - self.gameboard.x_chunk_multiplier) ** 2
            / self.gameboard.x_chunk_multiplier
            + (player_pos[1] - self.gameboard.y_chunk_multiplier) ** 2
            / self.gameboard.y_chunk_multiplier
        )

        features.append(distance_to_end)

        features = [feature / 1000000 for feature in features]

        return np.array(features)

    def __approximate(self, features):
        return np.dot(self.weights.astype(np.float64), features.astype(np.float64))

    def calculate_error(self, reward, player_pos, cars_pos, next_state):
        current_player_pos = player_pos
        current_cars_pos = cars_pos
        old_features = self.__prepare_features(
            current_player_pos,
            current_cars_pos,
        )
        future_cars = next_state.get_active_cars_pos()

        try:
            possible_actions = self.possible_actions[str(future_cars)][
                str(next_state.players[0].get_player_pos())
            ]
        except:
            return -10

        action_val_dict = {}
        for action in possible_actions:
            if action == "r":
                next_player_pos = [current_player_pos[0], current_player_pos[1] + 1]
            elif action == "l":
                next_player_pos = [current_player_pos[0], current_player_pos[1] - 1]
            elif action == "u":
                next_player_pos = [current_player_pos[0] - 1, current_player_pos[1]]
            elif action == "d":
                next_player_pos = [current_player_pos[0] + 1, current_player_pos[1]]
            else:
                next_player_pos = current_player_pos

            features = self.__prepare_features(next_player_pos, future_cars)
            action_val_dict[action] = self.__approximate(features)

        best_action = max(action_val_dict, key=lambda k: action_val_dict[k])

        return (
            reward
            + self.alpha * self.__approximate(action_val_dict[best_action])
            - self.__approximate(old_features)
        )

    def update(self, reward, player_pos, cars_pos, next_state):
        delta = self.calculate_error(reward, player_pos, cars_pos, next_state)
        upd = self.alpha * delta * self.features_num
        self.weights += upd
        self.__save_weigths()

    def get_best_action(self):
        current_player_pos = self.player.get_player_pos()
        current_cars_pos = self.gameboard.get_active_cars_pos()
        possible_actions = self.possible_actions[str(current_cars_pos)][
            str(current_player_pos)
        ]

        action_val_dict = {}
        for action in possible_actions:
            features = self.__prepare_features(current_player_pos, current_cars_pos)
            action_val_dict[action] = self.__approximate(features)

        best_value = max(action_val_dict.values())
        best_actions = [
            action for action, value in action_val_dict.items() if value == best_value
        ]

        # If there are multiple actions with the same maximum value, choose one randomly
        best_action = random.choice(best_actions)

        return best_action

    def get_action(self):
        r = np.random.random()
        if r > self.epsilon:
            return random.choice(
                self.possible_actions[str(self.gameboard.get_active_cars_pos())][
                    str(self.player.get_player_pos())
                ]
            )

        return self.get_best_action()

    def take_action(self):
        if self.counter == 7:
            self.counter = 0
            if self.is_training:
                cr_player_pos = self.player.get_player_pos()
                cr_cars_pos = self.gameboard.get_active_cars_pos()

                state_copy = deepcopy(self.gameboard)
                player_copy = deepcopy(self.player)
                state_copy.players = [player_copy]

                state_copy.init_cars()
                state_copy.move_cars()
                state_copy.update_reward_map()

                if self.player.is_dead:
                    print("ZMARL", self.player.player_kill_place)
                    self.player.reset_pos()
                    self.update(
                        -10,
                        self.player.player_kill_place,
                        self.player.cars_set_player_kill,
                        self.gameboard,
                    )
                elif self.player.has_won:
                    print("WYGRAL", cr_player_pos)
                    self.update(10, cr_player_pos, cr_cars_pos, state_copy)
                    self.player.reset_pos()
                else:
                    self.update(0, cr_player_pos, cr_cars_pos, state_copy)

                action = self.get_action()
            else:
                if self.player.is_dead or self.player.has_won:
                    self.player.reset_pos()

                action = self.get_best_action()

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
        else:
            self.counter += 1
