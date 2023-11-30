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

    gameboard.init_cars()

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_SPACE]:
                game_screen.change_lattice_visibility()
            if keys[pygame.K_DOWN]:
                player.go_down()
            if keys[pygame.K_RIGHT]:
                player.go_right()
            if keys[pygame.K_LEFT]:
                player.go_left()

        if gameboard.check_is_win() or gameboard.check_is_lose():
            running = False

        gamestate = gameboard.get_env_state()
        game_screen.set_gamestate(gamestate)
        game_screen.set_player_dir(player.get_player_dir())

        gameboard.init_cars()
        gameboard.move_cars()
        gameboard.get_possible_actions()

        game_screen.run_screen()


if __name__ == "__main__":
    main()
