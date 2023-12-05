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
            self.possible_actions = [self.go_right, self.go_down]
        else:
            self.dir = PLAYER_DIR_LEFT
            self.possible_actions = [self.go_left, self.go_down]

        self.player_type = player_type

        self.is_dead = False

    def __swap_direction(self, action):
        if action == self.go_right and self.dir == PLAYER_DIR_LEFT:
            self.dir = PLAYER_DIR_RIGHT
        if action == self.go_left and self.dir == PLAYER_DIR_RIGHT:
            self.dir = PLAYER_DIR_LEFT

    def go_right(self):
        if self.go_right in self.possible_actions:
            self.__swap_direction(self.go_right)
            self.prv_position = position
            self.position = [self.position[0], self.position[1] + 1]

    def go_left(self):
        if self.go_left in self.possible_actions:
            self.__swap_direction(self.go_left)
            self.prv_position = position
            self.position = [self.position[0], self.position[1] - 1]

    def go_down(self):
        if self.go_down in self.possible_actions:
            self.prv_position = position
            self.position = [self.position[0] + 1, self.position[1]]

    def get_old_pos(self):
        return self.prv_position

    def get_player_pos(self):
        return self.position

    def get_player_type(self):
        return self.player_type

    def update_possible_actions(self, possible_moves: list[str]):
        poss_actions = []

        if not self.is_dead:
            if "r" in possible_moves:
                poss_actions.append(self.go_right)

            if "l" in possible_moves:
                poss_actions.append(self.go_left)

            if "d" in possible_moves:
                poss_actions.append(self.go_down)

        self.possible_actions = poss_actions

    def get_possible_actions(self):
        return self.possible_actions

    def kill_player(self):
        self.is_dead = True
        self.position = [-1, -1]

    def take_action(self, action):
        action()
