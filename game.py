import pygame
from screen import Screen
from gameboard import Gameboard


def main():
    pygame.init()
    game_screen = Screen()
    running = True
    i = 0
    game_screen.change_lattice_visibility()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                game_screen.change_lattice_visibility()

        print(Gameboard().get_env_state())
        game_screen.run_screen()


if __name__ == "__main__":
    main()
