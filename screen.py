import pygame
from consts import (
    SCREEN_SIZE,
    SCREEN_CAPTION,
    FPS_MAX,
    GAME_CHUNK_SIZE,
    WHITE,
    BLACK,
    X_CHUNK_SIZE,
    Y_CHUNK_SIZE,
    ROAD_IMAGE,
    SIDEWALK_IMAGE,
)


class Screen:
    def __init__(self):
        self.display = pygame.display
        self.display.set_caption(SCREEN_CAPTION)
        self.screen = self.display.set_mode(SCREEN_SIZE)

        self.screen_rect = None
        self.drawable_elements = []

        self.clock = pygame.time.Clock()

        self.show_lattice = False

        self.x_chunk_multiplier = X_CHUNK_SIZE
        self.y_chunk_multiplier = Y_CHUNK_SIZE

        self.game_state = None
        self.map_state = None

    def __main_screen_update(self):
        self.screen_rect = self.screen.get_rect()
        self.screen.fill(BLACK)
        self.__draw_map()
        self.__update_elements()

        if self.show_lattice:
            self.draw_divided_screen()

        self.display.flip()
        self.clock.tick(FPS_MAX)

    def __update_elements(self):
        if len(self.drawable_elements) == 0:
            return
        for element in self.drawable_elements:
            element_to_draw = element[0]
            pos = element[1]
            self.screen.blit(element_to_draw, pos)

    def __draw_map(self):
        start_y = 0
        for i in range(self.y_chunk_multiplier):
            start_x = 0
            for j in range(self.x_chunk_multiplier):
                if self.map_state[i][j] == 0:
                    self.screen.blit(SIDEWALK_IMAGE, (start_x, start_y))
                else:
                    self.screen.blit(ROAD_IMAGE, (start_x, start_y))
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
        print(self.map_state)
