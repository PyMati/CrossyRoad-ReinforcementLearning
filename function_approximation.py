from copy import deepcopy
from traceback import print_tb
from turtle import pos
from player import Player
from gameboard import Gameboard
import random
from consts import X_CHUNK_SIZE, Y_CHUNK_SIZE
from sklearn.ensemble import RandomForestClassifier
import numpy as np


class ApproximationAgent:
    def __init__(self, gameboard: Gameboard, player: Player, train: bool):
        self.is_training = train
        self.decision_tree = RandomForestClassifier()

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
        if self.counter == 7:
            self.counter = 0
            if self.player.is_dead:
                self.player.reset_pos()
            current_player_pos = self.player.get_player_pos()
            map_state = self.gameboard.get_cars_pos()

            features = np.array(
                [
                    current_player_pos[0],
                    current_player_pos[1],
                    self.car_states_map[str(map_state)],
                ]
            )

            X = features.reshape(1, -1)

            if self.is_training:
                _, action = self.get_best_action()

                self.decision_tree.fit(X=X, y=[self.actions_numbers_classes[action]])

            action_num = int(self.decision_tree.predict(X)[0])
            real_action = self.numbers_actions_classes[action_num]
            self.__make_action(real_action)
        else:
            self.counter += 1

    def get_best_action(self):
        current_player_pos = self.player.get_player_pos()
        cars_pos = self.gameboard.get_cars_pos()
        possible_moves = self.possible_actions[str(cars_pos)][str(current_player_pos)]

        scores = []

        for move in possible_moves:
            next_player_pos = current_player_pos.copy()
            if move == "u":
                next_player_pos[0] -= 1
            elif move == "d":
                next_player_pos[0] += 1
            elif move == "l":
                next_player_pos[1] -= 1
            elif move == "r":
                next_player_pos[1] += 1
            else:
                pass

            scores.append(
                self.reward_maps[str(cars_pos)][next_player_pos[0]][next_player_pos[1]]
            )

        max_score = max(scores)
        max_move = possible_moves[scores.index(max_score)]

        return max_score, max_move

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
