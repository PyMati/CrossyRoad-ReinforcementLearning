from hmac import new
from re import S
from turtle import pos
import pygame
import numpy as np
import random
from car import Car
from consts import (
    OBSTACLE_NUM,
    X_CHUNK_SIZE,
    Y_CHUNK_SIZE,
    FINISH_NUM,
    PLAYER_NUM,
    OBSTACLE_CHANCE,
    OBSTACLE_NUM,
    LEFT_CAR_NUM,
    RIGHT_CAR_NUM,
    CAR_CHANCE,
)
from player import Player


class Gameboard(pygame.sprite.Sprite):
    def __init__(self, players: list[Player]):
        super(Gameboard, self).__init__()
        self.x_chunk_multiplier = X_CHUNK_SIZE
        self.y_chunk_multiplier = Y_CHUNK_SIZE

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

        self.map_env = np.zeros((self.y_chunk_multiplier, self.x_chunk_multiplier))
        self.__prepare_map()
        # Setting finish line
        self.map_env[self.y_chunk_multiplier - 1][self.end_x_pos] = FINISH_NUM

    def __prepare_map(self):
        for i in range(self.y_chunk_multiplier):
            if i % 2 == 1:
                self.road = np.ones((self.x_chunk_multiplier))
                self.map_env[i] = self.road
                self.cars_lanes_indexes.append(i)
            else:
                self.sidewalk = np.zeros((self.x_chunk_multiplier))
                if random.random() < OBSTACLE_CHANCE and i != 0:
                    obstacle_index = random.randint(0, self.x_chunk_multiplier - 1)
                    self.env[i][obstacle_index] = OBSTACLE_NUM
                self.map_env[i] = self.sidewalk

    def get_env_state(self):
        return self.env

    def get_map_state(self):
        return self.map_env

    def init_cars(self):
        if self.car_spawn_counter > 5:
            for i in self.cars_lanes_indexes:
                if LEFT_CAR_NUM not in self.env[i] and RIGHT_CAR_NUM not in self.env[i]:
                    if random.random() < CAR_CHANCE:
                        self.active_cars.append(Car(i))
            self.car_spawn_counter = 0
        else:
            self.car_spawn_counter += 1

    def move_cars(self):
        self.__clear_cars()
        if self.car_counter > 10:
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

    def update_possible_players_actions(self):
        for player in self.players:
            position = player.get_player_pos()

            x = position[1]
            y = position[0]

            actions = []
            actions += self.__can_go_down(x, y)
            actions += self.__can_go_right(x, y)
            actions += self.__can_go_left(x, y)

            player.update_possible_actions(actions)

    def check_end_game(self):
        dead_players = 0
        for player in self.players:
            if player.get_player_pos() == [self.y_chunk_multiplier - 1, self.end_x_pos]:
                return player.get_player_type()
            if player.is_dead:
                dead_players += 1

        if dead_players == len(self.players):
            return "env"

        return False

    def check_collision(self):
        for player in self.players:
            for car in self.active_cars:
                if player.get_player_pos() == car.get_pos():
                    player.kill_player()
