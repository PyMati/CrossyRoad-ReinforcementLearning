import pygame
import random
from consts import (
    GAME_CHUNK_SIZE,
    LEFT_CAR_NUM,
    RIGHT_CAR_NUM,
    OBSTACLE_CHANCE,
    X_CHUNK_SIZE,
)


class Car(pygame.sprite.Sprite):
    def __init__(self, lane: int):
        super(Car, self).__init__()

        self.prv_pos = [lane, 0]

        self.dir = RIGHT_CAR_NUM
        self.pos = [lane, X_CHUNK_SIZE]

    def get_pos(self):
        return self.pos

    def check_state(self):
        if self.pos[1] >= X_CHUNK_SIZE or self.pos[1] < 0:
            self.kill()

    def move(self):
        self.prv_pos = self.pos
        if self.dir == RIGHT_CAR_NUM:
            self.pos = [self.pos[0], self.pos[1] - 1]
        else:
            self.pos = [self.pos[0], self.pos[1] + 1]
