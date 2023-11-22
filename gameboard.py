from hmac import new
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
    CAR_NUM,
    CAR_CHANCE,
)


class Gameboard(pygame.sprite.Sprite):
    def __init__(self):
        super(Gameboard, self).__init__()
        self.x_chunk_multiplier = X_CHUNK_SIZE
        self.y_chunk_multiplier = Y_CHUNK_SIZE

        self.end_x_pos = random.randint(0, self.x_chunk_multiplier - 1)

        self.is_win = False

        self.cars_lanes_indexes = []
        self.active_cars: list[Car] = []
        self.car_counter = 0
        self.car_spawn_counter = 0

        # Setting player env
        self.env = np.zeros((self.y_chunk_multiplier, self.x_chunk_multiplier))
        # Setting finish line
        self.env[self.y_chunk_multiplier - 1][self.end_x_pos] = FINISH_NUM
        # Setting player start position
        self.env[0][0] = PLAYER_NUM

        self.map_env = np.zeros((self.y_chunk_multiplier, self.x_chunk_multiplier))
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
        # Setting finish line
        self.map_env[self.y_chunk_multiplier - 1][self.end_x_pos] = FINISH_NUM

    def get_env_state(self):
        return self.env

    def get_map_state(self):
        return self.map_env

    def is_legal(self, newpos) -> bool:
        newy = newpos[0]
        newx = newpos[1]
        if newy < 0 or newy >= self.y_chunk_multiplier:
            return False
        if newx < 0 or newx >= self.x_chunk_multiplier:
            return False
        if self.env[newy][newx] == OBSTACLE_NUM:
            return False
        return True

    def change_player_pos(self, oldpos: tuple, newpos: tuple):
        self.env[oldpos[0]][oldpos[1]] = 0
        self.env[newpos[0]][newpos[1]] = PLAYER_NUM

    def check_is_win(self) -> bool:
        if self.env[self.y_chunk_multiplier - 1][self.end_x_pos] == PLAYER_NUM:
            return True
        return False

    def check_is_lose(self) -> bool:
        if PLAYER_NUM not in self.env:
            return True
        return False

    def init_cars(self):
        if self.car_spawn_counter > 5:
            for i in self.cars_lanes_indexes:
                if CAR_NUM not in self.env[i]:
                    if random.random() < CAR_CHANCE:
                        self.active_cars.append(Car(i))
            self.car_spawn_counter = 0
        else:
            self.car_spawn_counter += 1

    def move_cars(self):
        if self.car_counter > 10:
            for car in self.active_cars:
                car.check_state()
                car.move()
                oldpos = car.prv_pos
                newpos = car.pos
                if self.is_legal(oldpos):
                    self.env[oldpos[0]][oldpos[1]] = 0
                if self.is_legal(newpos):
                    self.env[newpos[0]][newpos[1]] = CAR_NUM
            self.car_counter = 0
        else:
            self.car_counter += 1
