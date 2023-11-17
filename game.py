import pygame
from screen import Screen


def main():
    pygame.init()
    game_screen = Screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game_screen.run_screen()


if __name__ == "__main__":
    main()
