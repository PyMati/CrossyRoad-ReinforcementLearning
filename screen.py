import pygame
from consts import SCREEN_SIZE, SCREEN_CAPTION, FPS_MAX, BLACK, GAME_CHUNK_SIZE
import numpy


class Screen:
    def __init__(self):
        self.display = pygame.display
        self.display.set_caption(SCREEN_CAPTION)
        self.screen_rect = None
        self.drawable_elements = []

        self.clock = pygame.time.Clock()

        self.x_chunk_multiplier = int(SCREEN_SIZE[0] / GAME_CHUNK_SIZE)
        self.y_chunk_multiplier = int(SCREEN_SIZE[1] / GAME_CHUNK_SIZE)

        self.gameState = numpy.ones(
            (self.x_chunk_multiplier, self.y_chunk_multiplier))

        print(self.gameState)

        self.__main_screen_update()

    def __main_screen_update(self):
        self.screen = self.display.set_mode(SCREEN_SIZE)
        self.screen_rect = self.screen.get_rect()
        self.__update_elements()
        self.clock.tick(FPS_MAX)
        self.screen.fill(BLACK)
        self.display.flip()

    def __update_elements(self):
        if len(self.drawable_elements) == 0:
            return
        for element in self.drawable_elements:
            element_to_draw = element[0]
            pos = element[1]
            self.screen.blit(element_to_draw, pos)

    def draw_divided_screen(self):
        return

    def run_screen(self):
        self.__main_screen_update()

    def get_screen_rect(self):
        if self.screen_rect == None:
            return (0, 0, 0, 0)
        return self.screen_rect
