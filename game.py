import pygame
from screen import Screen
from gameboard import Gameboard
from player import Player


def main():
    pygame.init()

    gameboard = Gameboard()
    player = Player(gameboard)
    game_screen = Screen()

    gamestate = gameboard.get_env_state()
    gamemap = gameboard.get_map_state()

    game_screen.set_gamestate(gamestate)
    game_screen.set_map(gamemap)
    game_screen.set_player_dir(player.get_player_dir())

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_SPACE]:
                game_screen.change_lattice_visibility()
            if keys[pygame.K_s]:
                player.go_down()
            if keys[pygame.K_d]:
                player.go_right()
            if keys[pygame.K_a]:
                player.go_left()

        gamestate = gameboard.get_env_state()
        game_screen.set_gamestate(gamestate)
        game_screen.set_player_dir(player.get_player_dir())

        game_screen.run_screen()


if __name__ == "__main__":
    main()
