import pygame
import numpy as np
from screen import Screen
from consts import X_CHUNK_SIZE, Y_CHUNK_SIZE, ROAD_IMAGE, GAME_CHUNK_SIZE


class Gameboard(pygame.sprite.Sprite):
    def __init__(self, screen: Screen):
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
        self.env = np.zeros((self.x_chunk_multiplier, self.y_chunk_multiplier))

        self.screen = screen

    def get_env_state(self):
        return self.env

    def get_map_state(self):
        return self.map_env
