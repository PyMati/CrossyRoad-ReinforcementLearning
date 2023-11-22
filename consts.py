import pygame

# Screen options
SCREEN_SIZE = (480, 640)
SCREEN_CAPTION = "AICrossy Road"
FPS_MAX = 60

# Color options
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game options
GAME_CHUNK_SIZE = 40
X_CHUNK_SIZE = int(SCREEN_SIZE[0] / GAME_CHUNK_SIZE)
Y_CHUNK_SIZE = int(SCREEN_SIZE[1] / GAME_CHUNK_SIZE)

# Images loading
SIZE = (GAME_CHUNK_SIZE, GAME_CHUNK_SIZE)
PLAYER_IMAGE = pygame.image.load("./FormattedAssets/Chicken.png")
PLAYER_IMAGE = pygame.transform.scale(
    PLAYER_IMAGE, (GAME_CHUNK_SIZE - 10, GAME_CHUNK_SIZE - 10)
)
PLAYER_NUM = -1
PLAYER_DIR_RIGHT = 1
PLAYER_DIR_LEFT = -1
SIDEWALK_IMAGE = pygame.image.load("./FormattedAssets/Sidewalk.png")
SIDEWALK_IMAGE = pygame.transform.scale(SIDEWALK_IMAGE, SIZE)
SIDE_NUM = 0
ROAD_IMAGE = pygame.image.load("./FormattedAssets/Road.png")
ROAD_IMAGE = pygame.transform.scale(ROAD_IMAGE, SIZE)
ROAD_NUM = 1
FINISH_IMAGE = pygame.image.load("./FormattedAssets/Finish.png")
FINISH_IMAGE = pygame.transform.scale(FINISH_IMAGE, SIZE)
FINISH_NUM = 3
