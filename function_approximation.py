from copy import deepcopy

from sklearn.exceptions import NotFittedError
from player import Player
from gameboard import Gameboard
from consts import X_CHUNK_SIZE, Y_CHUNK_SIZE
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle


class ApproximationAgent:
    def __init__(self, gameboard: Gameboard, player: Player, train: bool):
        self.is_training = train
        self.load_model()

        self.player = player
        self.gameboard = gameboard

        self.all_possible_car_states = 9
        self.possible_cars_pos = []
        self.reward_maps = {}
        self.car_states_map = {}

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

        self.__init_all_car_states()

        self.counter = 0

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.3

        self.episodes = 0

        self.states = []
        self.possible_actions = {}

        self.__init_vals()

        print(f"Settings: {self.alpha} {self.gamma} {self.epsilon}")

    def __init_all_car_states(self):
        gameboard_copy = deepcopy(self.gameboard)
        state_index = 0
        while len(self.possible_cars_pos) != self.all_possible_car_states:
            pos = gameboard_copy.get_cars_pos()
            if pos in self.possible_cars_pos:
                pass
            else:
                self.possible_cars_pos.append(pos)
                self.reward_maps[str(pos)] = gameboard_copy.reward_map.copy()
                self.car_states_map[str(pos)] = state_index
                state_index += 1

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

    def take_action(self):
        if self.counter == 10:
            self.counter = 0

            if self.player.is_dead:
                player_pos = self.player.get_old_pos()
            else:
                player_pos = self.player.get_player_pos()

            map_state = self.gameboard.get_cars_pos()

            features = np.array(
                [
                    player_pos[0],
                    player_pos[1],
                    self.car_states_map[str(map_state)],
                ]
            )

            X = features.reshape(1, -1)

            if self.is_training:
                try:
                    current_q_value = self.decision_tree.predict(X)
                except NotFittedError:
                    current_q_value = 0

                if self.player.is_dead:
                    reward = -10

                reward = self.reward_maps[str(
                    map_state)][str(player_pos)]

                self.decision_tree.fit(
                    X=X, y=[self.actions_numbers_classes[action]])

                _, action = self.get_action()

                self.save_model()

            # self.__make_action(real_action)
            if self.player.is_dead:
                self.player.reset_pos()
        else:
            self.counter += 1
            if self.player.is_dead:
                self.player.reset_pos()

    def get_best_next_q_value(self, map_state, player_pos):
        possible_actions = self.possible_actions[str(
            map_state)][str(player_pos)]
        print(possible_actions)

    # def update(self):
    #     current_player_pos = self.player.get_player_pos()
    #     cars_pos = self.gameboard.get_cars_pos()
    #     possible_moves = self.possible_actions[str(
    #         cars_pos)][str(current_player_pos)]

    #     scores = {}
    #     all_moves = ["u", "d", "l", "r", "u"]

    #     new_q_value = current_q_value + self.alpha * (
    #         reward + self.gamma * max_next_q_value - current_q_value
    #     )

    #     for move in possible_moves:
    #         next_player_pos = current_player_pos.copy()
    #         if move == "u":
    #             next_player_pos[0] -= 1
    #         elif move == "d":
    #             next_player_pos[0] += 1
    #         elif move == "l":
    #             next_player_pos[1] -= 1
    #         elif move == "r":
    #             next_player_pos[1] += 1
    #         else:
    #             pass

    #         scores[move] = self.reward_maps[str(cars_pos)
    #                                         ][next_player_pos[0]][next_player_pos[1]]

    #     for move in all_moves:
    #         if move not in scores.keys():
    #             scores[move] = 0

    #     return scores, possible_moves

    def __make_action(self, action):
        if action == "u":
            self.player.go_up()
        elif action == "d":
            self.player.go_down()
        elif action == "l":
            self.player.go_left()
        elif action == "r":
            self.player.go_right()
        else:
            pass

    def save_model(self, model_filename="model.pkl"):
        if self.is_training:
            with open(model_filename, 'wb') as model_file:
                pickle.dump(self.decision_tree, model_file)
            print(f"Model saved as {model_filename}")

    def load_model(self, model_filename="model.pkl"):
        try:
            with open(model_filename, 'rb') as model_file:
                self.decision_tree = pickle.load(model_file)
            print(f"Model loaded from {model_filename}")
        except FileNotFoundError:
            self.decision_tree = RandomForestClassifier()
            print(
                f"Model file '{model_filename}' not found. Training a new model.")
