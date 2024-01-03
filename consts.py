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

GAME_CHUNK_SIZE = 80
X_CHUNK_SIZE = int(SCREEN_SIZE[0] / GAME_CHUNK_SIZE)
Y_CHUNK_SIZE = int(SCREEN_SIZE[1] / GAME_CHUNK_SIZE)
OBSTACLE_CHANCE = 0.5
CAR_CHANCE = 0.2

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

OBSTACLE_IMAGE = pygame.image.load("./FormattedAssets/obstacle.png")
OBSTACLE_IMAGE = pygame.transform.scale(
    OBSTACLE_IMAGE, (GAME_CHUNK_SIZE - 10, GAME_CHUNK_SIZE - 10)
)
OBSTACLE_NUM = 5

CAR_IMAGE = pygame.image.load("./FormattedAssets/Car.png")
CAR_IMAGE = pygame.transform.scale(
    CAR_IMAGE, (GAME_CHUNK_SIZE - 2.5, GAME_CHUNK_SIZE - 2.5)
)
LEFT_CAR_NUM = 6
RIGHT_CAR_NUM = 7

STARTING_POSITIONS = [[0, X_CHUNK_SIZE // 2], [0, X_CHUNK_SIZE // 2]]
REAL_PLAYER_POS = STARTING_POSITIONS[0]
AGENT_POS = STARTING_POSITIONS[1]
PASSIVE_AGENT = [0, 0]

# Rewards
FINISH_LINE_REWARD = 100
CAR_REWARD = -10

# Static map settings y 0 - 7 / x 0 - 5
STATIC_CARS_POS = [[1, 3], [1, 4], [3, 2], [3, 1], [5, 3], [5, 2]]
