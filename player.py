import pygame
from gameboard import Gameboard
from consts import PLAYER_DIR_LEFT, PLAYER_DIR_RIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, gameboard: Gameboard):
        super(Player, self).__init__()
        self.gameboard = gameboard
        self.prv_position = [0, 0]
        self.position = [0, 0]
        self.dir = PLAYER_DIR_RIGHT

    def go_down(self):
        new_pos = [self.position[0] + 1, self.position[1]]
        if self.gameboard.is_legal(new_pos):
            self.prv_position = self.position
            self.position = new_pos
            self.gameboard.change_player_pos(self.prv_position, self.position)

    def go_right(self):
        new_pos = [self.position[0], self.position[1] + 1]
        if self.gameboard.is_legal(new_pos):
            if self.dir == PLAYER_DIR_LEFT:
                self.dir = PLAYER_DIR_RIGHT
            self.prv_position = self.position
            self.position = new_pos
            self.gameboard.change_player_pos(self.prv_position, self.position)

    def go_left(self):
        new_pos = [self.position[0], self.position[1] - 1]
        if self.gameboard.is_legal(new_pos):
            if self.dir == PLAYER_DIR_RIGHT:
                self.dir = PLAYER_DIR_LEFT
            self.prv_position = self.position
            self.position = new_pos
            self.gameboard.change_player_pos(self.prv_position, self.position)

    def get_player_dir(self):
        return self.dir
