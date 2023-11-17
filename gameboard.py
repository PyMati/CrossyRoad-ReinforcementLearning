import pygame
import numpy as np
from consts import X_CHUNK_SIZE, Y_CHUNK_SIZE


class Gameboard:
    def __init__(self):
        self.x_chunk_multiplier = X_CHUNK_SIZE
        self.y_chunk_multiplier = Y_CHUNK_SIZE

        self.env = np.zeros((self.x_chunk_multiplier, self.y_chunk_multiplier))

    def get_env_state(self):
        return self.env
