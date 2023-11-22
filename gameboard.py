from hmac import new
import pygame
import numpy as np
from screen import Screen
from consts import X_CHUNK_SIZE, Y_CHUNK_SIZE, FINISH_NUM, PLAYER_NUM


class Gameboard(pygame.sprite.Sprite):
    def __init__(self):
        super(Gameboard, self).__init__()
        self.x_chunk_multiplier = X_CHUNK_SIZE
        self.y_chunk_multiplier = Y_CHUNK_SIZE

        self.map_env = np.zeros((self.y_chunk_multiplier, self.x_chunk_multiplier))
        for i in range(self.y_chunk_multiplier):
            if i % 2 == 1:
                self.road = np.ones((self.x_chunk_multiplier))
                self.map_env[i] = self.road
            else:
                self.sidewalk = np.zeros((self.x_chunk_multiplier))
                self.map_env[i] = self.sidewalk
        self.env = np.zeros((self.y_chunk_multiplier, self.x_chunk_multiplier))
        # Setting finish line
        self.env[self.y_chunk_multiplier - 1][self.x_chunk_multiplier - 1] = FINISH_NUM
        self.map_env[self.y_chunk_multiplier - 1][
            self.x_chunk_multiplier - 1
        ] = FINISH_NUM
        # Setting player start position
        self.env[0][0] = PLAYER_NUM

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
        return True

    def change_player_pos(self, oldpos: tuple, newpos: tuple):
        self.env[oldpos[0]][oldpos[1]] = 0
        self.env[newpos[0]][newpos[1]] = PLAYER_NUM
