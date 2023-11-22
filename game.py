import pygame
from screen import Screen
from gameboard import Gameboard


def main():
    pygame.init()

    game_screen = Screen()
    gameboard = Gameboard(game_screen)

    gamestate = gameboard.get_env_state()
    gamemap = gameboard.get_map_state()

    game_screen.set_gamestate(gamestate)
    game_screen.set_map(gamemap)

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_w]:
                game_screen.change_lattice_visibility()

        game_screen.run_screen()


if __name__ == "__main__":
    main()
