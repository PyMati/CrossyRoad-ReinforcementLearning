import pygame
import random
from consts import (
    GAME_CHUNK_SIZE,
    PLAYER_DIR_LEFT,
    PLAYER_DIR_RIGHT,
    OBSTACLE_CHANCE,
    X_CHUNK_SIZE,
)


class Car(pygame.sprite.Sprite):
    def __init__(self, lane: int):
        super(Car, self).__init__()

        self.prv_pos = [lane, 0]

        if random.random() > OBSTACLE_CHANCE:
            self.dir = PLAYER_DIR_RIGHT
            self.pos = [lane, 0]
        else:
            self.dir = PLAYER_DIR_LEFT
            self.pos = [lane, X_CHUNK_SIZE - 1]

    def get_pos(self):
        return self.pos

    def check_state(self):
        if self.pos[1] >= GAME_CHUNK_SIZE or self.pos[1] < 0:
            self.kill()

    def move(self):
        self.prv_pos = self.pos
        if self.dir == PLAYER_DIR_LEFT:
            self.pos = [self.pos[0], self.pos[1] - 1]
        else:
            self.pos = [self.pos[0], self.pos[1] + 1]
