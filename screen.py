import pygame
from consts import (
    PLAYER_NUM,
    SCREEN_SIZE,
    SCREEN_CAPTION,
    FPS_MAX,
    GAME_CHUNK_SIZE,
    WHITE,
    BLACK,
    X_CHUNK_SIZE,
    Y_CHUNK_SIZE,
    SIDEWALK_IMAGE,
    ROAD_IMAGE,
    FINISH_IMAGE,
    SIDE_NUM,
    ROAD_NUM,
    FINISH_NUM,
    PLAYER_IMAGE,
    PLAYER_DIR_RIGHT,
    OBSTACLE_IMAGE,
    OBSTACLE_NUM,
)


class Screen:
    def __init__(self):
        self.display = pygame.display
        self.display.set_caption(SCREEN_CAPTION)
        self.screen = self.display.set_mode(SCREEN_SIZE)

        self.screen_rect = None

        self.clock = pygame.time.Clock()

        self.show_lattice = False

        self.x_chunk_multiplier = X_CHUNK_SIZE
        self.y_chunk_multiplier = Y_CHUNK_SIZE

        self.game_state = None
        self.map_state = None

        self.player_dir = None

    def __main_screen_update(self):
        self.screen_rect = self.screen.get_rect()
        self.screen.fill(BLACK)
        self.__draw_map()
        self.__draw_players()
        self.__draw_obstacles()

        if self.show_lattice:
            self.draw_divided_screen()

        self.display.flip()
        self.clock.tick(FPS_MAX)

    def __draw_map(self):
        start_y = 0
        for i in range(self.y_chunk_multiplier):
            start_x = 0
            for j in range(self.x_chunk_multiplier):
                pos = (start_x, start_y)
                map_val = self.map_state[i][j]
                if map_val == SIDE_NUM:
                    self.screen.blit(SIDEWALK_IMAGE, pos)
                elif map_val == ROAD_NUM:
                    self.screen.blit(ROAD_IMAGE, pos)
                elif map_val == FINISH_NUM:
                    self.screen.blit(FINISH_IMAGE, pos)
                start_x += GAME_CHUNK_SIZE
            start_y += GAME_CHUNK_SIZE

    def __draw_players(self):
        start_y = 0
        for i in range(self.y_chunk_multiplier):
            start_x = 0
            for j in range(self.x_chunk_multiplier):
                pos = (start_x, start_y)
                map_val = self.game_state[i][j]
                if map_val == PLAYER_NUM:
                    if self.player_dir == PLAYER_DIR_RIGHT:
                        self.screen.blit(PLAYER_IMAGE, pos)
                    else:
                        self.screen.blit(
                            pygame.transform.flip(PLAYER_IMAGE, True, False), pos
                        )
                start_x += GAME_CHUNK_SIZE
            start_y += GAME_CHUNK_SIZE

    def __draw_obstacles(self):
        start_y = 0
        for i in range(self.y_chunk_multiplier):
            start_x = 0
            for j in range(self.x_chunk_multiplier):
                pos = (start_x, start_y)
                map_val = self.game_state[i][j]
                if map_val == OBSTACLE_NUM:
                    self.screen.blit(OBSTACLE_IMAGE, pos)
                start_x += GAME_CHUNK_SIZE
            start_y += GAME_CHUNK_SIZE

    def draw_divided_screen(self):
        start_x = 0
        for _ in range(self.x_chunk_multiplier):
            start_y = 0
            for _ in range(self.y_chunk_multiplier):
                chunk = pygame.Rect(start_x, start_y, GAME_CHUNK_SIZE, GAME_CHUNK_SIZE)
                pygame.draw.rect(self.screen, WHITE, chunk, 1)
                start_y += GAME_CHUNK_SIZE
            start_x += GAME_CHUNK_SIZE

    def run_screen(self):
        self.__main_screen_update()

    def get_screen_rect(self):
        if self.screen_rect == None:
            return (0, 0, 0, 0)
        return self.screen_rect

    def change_lattice_visibility(self):
        if not self.show_lattice:
            self.show_lattice = True
        else:
            self.show_lattice = False

    def set_gamestate(self, gamestate):
        self.game_state = gamestate

    def set_map(self, mapstate):
        self.map_state = mapstate

    def set_player_dir(self, playerdir):
        self.player_dir = playerdir
