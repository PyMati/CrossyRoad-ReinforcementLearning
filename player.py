from turtle import position
import pygame
from consts import PLAYER_DIR_LEFT, PLAYER_DIR_RIGHT, REAL_PLAYER_POS


class Player(pygame.sprite.Sprite):
    def __init__(self, position: list[int], player_type: str):
        super(Player, self).__init__()
        self.prv_position = position
        self.position = position
        if self.position == REAL_PLAYER_POS:
            self.dir = PLAYER_DIR_RIGHT
        else:
            self.dir = PLAYER_DIR_LEFT

        self.player_type = player_type

    def go_right(self):
        self.prv_position = position
        self.position = [self.position[0], self.position[1] + 1]

    def go_left(self):
        self.prv_position = position
        self.position = [self.position[0], self.position[1] - 1]

    def go_down(self):
        self.prv_position = position
        self.position = [self.position[0] + 1, self.position[1]]

    def get_old_pos(self):
        return self.prv_position

    def get_player_pos(self):
        return self.position

    def get_player_type(self):
        return self.player_type
