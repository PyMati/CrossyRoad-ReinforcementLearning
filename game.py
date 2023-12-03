from numpy import real
import pygame
from screen import Screen
from gameboard import Gameboard
from consts import REAL_PLAYER_POS, AGENT_POS
from player import Player
import random


# TODO: Wykryj, ktory gracz wygral
# TODO: Postaraj sie juz zaczac pisac monte carlo
def main():
    pygame.init()

    agent = Player(AGENT_POS, "agent")
    real_player = Player(REAL_PLAYER_POS, "real")
    players = [agent, real_player]

    gameboard = Gameboard(players)
    game_screen = Screen(players)

    gamestate = gameboard.get_env_state()
    gamemap = gameboard.get_map_state()

    game_screen.set_gamestate(gamestate)
    game_screen.set_map(gamemap)

    gameboard.init_cars()

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_SPACE]:
                game_screen.change_lattice_visibility()
            if keys[pygame.K_RIGHT]:
                real_player.go_right()
            if keys[pygame.K_LEFT]:
                real_player.go_left()
            if keys[pygame.K_DOWN]:
                real_player.go_down()

        if type(gameboard.check_end_game()) == str:
            print(gameboard.check_end_game(), "won")
            running = False

        gamestate = gameboard.get_env_state()
        game_screen.set_gamestate(gamestate)

        action = random.choice(agent.get_possible_actions())
        action()

        gameboard.update_possible_players_actions()

        gameboard.init_cars()
        gameboard.move_cars()

        game_screen.run_screen()


if __name__ == "__main__":
    main()
