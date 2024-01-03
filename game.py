from numpy import real
import pygame
from screen import Screen
from gameboard import Gameboard
from consts import REAL_PLAYER_POS, AGENT_POS, PASSIVE_AGENT
from player import Player
from monte_carlo_agent import MonteCarloAgent
from passive_learning_agent import PassiveLearningAgent


def main():
    pygame.init()

    # Change if you want to use monte carlo agent
    static_map: bool = True

    agent = Player(AGENT_POS, "agent")
    real_player = Player(REAL_PLAYER_POS, "real")
    passive_agent = Player(PASSIVE_AGENT, "passive_agent")
    # players = [agent, real_player]
    players = [passive_agent]

    gameboard = Gameboard(players, static_map)
    game_screen = Screen(players)

    gamestate = gameboard.get_env_state()
    gamemap = gameboard.get_map_state()

    game_screen.set_gamestate(gamestate)
    game_screen.set_map(gamemap)

    gameboard.update_reward_map()
    psa = PassiveLearningAgent(gameboard, passive_agent)
    # monte_carlo_agent = MonteCarloAgent(agent, gameboard)

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
            if keys[pygame.K_UP]:
                real_player.go_up()

        if type(gameboard.check_end_game()) == str:
            print(gameboard.check_end_game(), "won")
            running = False

        gamestate = gameboard.get_env_state()
        game_screen.set_gamestate(gamestate)

        psa.take_action()
        # Monte carlo / runs only with static_map = False
        # monte_carlo_agent.play_game()

        gameboard.develop_game()

        game_screen.run_screen()


if __name__ == "__main__":
    main()
