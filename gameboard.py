from copy import deepcopy
from matplotlib.pylab import rand
import pygame
import numpy as np
import random
from car import Car
from consts import (
    CAR_REWARD,
    OBSTACLE_NUM,
    X_CHUNK_SIZE,
    Y_CHUNK_SIZE,
    FINISH_NUM,
    FINISH_LINE_REWARD,
    OBSTACLE_CHANCE,
    OBSTACLE_NUM,
    LEFT_CAR_NUM,
    RIGHT_CAR_NUM,
    CAR_CHANCE,
    STATIC_CARS_POS,
)
from player import Player


class Gameboard(pygame.sprite.Sprite):
    def __init__(self, players: list[Player], static_map: bool):
        super(Gameboard, self).__init__()
        self.x_chunk_multiplier = X_CHUNK_SIZE
        self.y_chunk_multiplier = Y_CHUNK_SIZE
        self.static_map = static_map

        if static_map:
            self.end_x_pos = self.x_chunk_multiplier - 1
        else:
            self.end_x_pos = random.randint(0, self.x_chunk_multiplier - 1)

        self.is_win = False

        self.players = players

        self.cars_lanes_indexes = []
        self.active_cars: list[Car] = []
        self.car_counter = 0
        self.car_spawn_counter = 0

        # Setting player env
        self.env = np.zeros((self.y_chunk_multiplier, self.x_chunk_multiplier))

        # Setting finish line
        self.env[self.y_chunk_multiplier - 1][self.end_x_pos] = FINISH_NUM

        # Setting reward graph
        self.reward_map = np.zeros((self.y_chunk_multiplier, self.x_chunk_multiplier))

        self.map_env = np.zeros((self.y_chunk_multiplier, self.x_chunk_multiplier))
        self.__prepare_map()
        # Setting finish line
        self.map_env[self.y_chunk_multiplier - 1][self.end_x_pos] = FINISH_NUM
        self.reward_map[self.y_chunk_multiplier - 1][
            self.end_x_pos
        ] = FINISH_LINE_REWARD

    def __prepare_map(self):
        for i in range(self.y_chunk_multiplier):
            if i % 2 == 1:
                self.road = np.ones((self.x_chunk_multiplier))
                self.map_env[i] = self.road
                self.cars_lanes_indexes.append(i)
            else:
                self.sidewalk = np.zeros((self.x_chunk_multiplier))
                if not self.static_map:
                    if random.random() < OBSTACLE_CHANCE and i != 0:
                        obstacle_index = random.randint(0, self.x_chunk_multiplier - 1)
                        self.env[i][obstacle_index] = OBSTACLE_NUM
                self.map_env[i] = self.sidewalk

        if self.static_map:
            for car_pos in STATIC_CARS_POS:
                self.reward_map[car_pos[0]][car_pos[1]] = CAR_REWARD
                self.env[car_pos[0]][car_pos[1]] = LEFT_CAR_NUM

    def get_env_state(self):
        return self.env

    def get_map_state(self):
        return self.map_env

    def update_reward_map(self):
        for i in range(self.y_chunk_multiplier):
            for j in range(self.x_chunk_multiplier):
                if self.reward_map[i][j] == FINISH_LINE_REWARD:
                    continue
                elif self.env[i][j] == RIGHT_CAR_NUM or self.env[i][j] == LEFT_CAR_NUM:
                    self.reward_map[i][j] = CAR_REWARD
                else:
                    # if not self.static_map:
                    self.reward_map[i][j] = (
                        FINISH_LINE_REWARD
                        - (
                            (j - self.end_x_pos) ** 2
                            + (i - (self.y_chunk_multiplier - 1)) ** 2
                        )
                    ) * 0.09
                # else:
                #     self.reward_map[i][j] = 0

    def init_cars(self):
        if self.car_spawn_counter > 5:
            for i in self.cars_lanes_indexes:
                if LEFT_CAR_NUM not in self.env[i] and RIGHT_CAR_NUM not in self.env[i]:
                    self.active_cars.append(Car(i))
            self.car_spawn_counter = 0
        else:
            self.car_spawn_counter += 1

    def move_cars(self):
        self.__clear_cars()
        if self.car_counter > 9:
            for car in self.active_cars:
                car.check_state()
                car.move()
                oldpos = car.prv_pos
                newpos = car.pos
                if oldpos[1] >= 0 and oldpos[1] < self.x_chunk_multiplier:
                    self.env[oldpos[0]][oldpos[1]] = 0
                if newpos[1] >= 0 and newpos[1] < self.x_chunk_multiplier:
                    self.env[newpos[0]][newpos[1]] = car.dir
            self.car_counter = 0
        else:
            self.car_counter += 1

    def __clear_cars(self):
        cars_to_remove = []
        for car in self.active_cars:
            if car.pos[1] < 0 or car.pos[1] > self.x_chunk_multiplier:
                cars_to_remove.append(car)

        for car in cars_to_remove:
            self.active_cars.remove(car)

    def get_active_cars_pos(self):
        return [car.pos for car in self.active_cars]

    def __can_go_right(self, x, y):
        if x != self.x_chunk_multiplier - 1 and self.env[y][x + 1] != OBSTACLE_NUM:
            return ["r"]
        return []

    def __can_go_left(self, x, y):
        if x != 0 and self.env[y][x - 1] != OBSTACLE_NUM:
            return ["l"]
        return []

    def __can_go_down(self, x, y):
        if y != self.y_chunk_multiplier - 1 and self.env[y + 1][x] != OBSTACLE_NUM:
            return ["d"]
        return []

    def __can_go_up(self, x, y):
        if y - 1 > -1 and self.env[y - 1][x] != OBSTACLE_NUM:
            return ["u"]
        return []

    def get_possible_actions(self, y, x):
        actions = []
        actions += self.__can_go_down(x, y)
        actions += self.__can_go_right(x, y)
        actions += self.__can_go_left(x, y)
        actions += self.__can_go_up(x, y)
        actions += ["s"]

        return actions

    def update_possible_players_actions(self):
        for player in self.players:
            position = player.get_player_pos()

            x = position[1]
            y = position[0]

            actions = []
            if not player.is_dead:
                actions += self.__can_go_down(x, y)
                actions += self.__can_go_right(x, y)
                actions += self.__can_go_left(x, y)
                actions += self.__can_go_up(x, y)
                actions += ["s"]

            player.update_possible_actions(actions)

    def check_end_game(self):
        dead_players = 0
        for player in self.players:
            if player.get_player_pos() == [self.y_chunk_multiplier - 1, self.end_x_pos]:
                player.has_won = True
                return player.get_player_type()
            if player.is_dead:
                dead_players += 1
            if player.has_won:
                return True

        if dead_players == len(self.players):
            return True

        return False

    def check_collision(self):
        for player in self.players:
            for car in self.active_cars:
                if player.get_player_pos() == car.get_pos() and player.has_won != True:
                    player.kill_player()

    def check_static_end(self):
        for player in self.players:
            for car_pos in STATIC_CARS_POS:
                if player.get_player_pos() == car_pos and player.has_won != True:
                    player.kill_player()

    def get_reward(self, player_pos):
        return self.reward_map[player_pos[0]][player_pos[1]]

    def develop_game(self):
        # self.check_end_game() odkomentuj po wytrenowaniu agenta
        if self.static_map:
            self.check_static_end()
        else:
            self.check_collision()
        self.update_possible_players_actions()
        if not self.static_map:
            self.init_cars()
            self.move_cars()
        self.update_reward_map()
