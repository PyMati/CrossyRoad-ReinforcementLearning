import pygame
from screen import Screen


def main():
    pygame.init()
    game_screen = Screen()
    while True:
        game_screen.run_screen()


if __name__ == "__main__":
    main()
