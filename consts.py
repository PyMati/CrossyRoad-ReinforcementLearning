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
ROAD_IMAGE = pygame.image.load("./FormattedAssets/Road.png")
ROAD_IMAGE = pygame.transform.scale(ROAD_IMAGE, (GAME_CHUNK_SIZE, GAME_CHUNK_SIZE))
SIDEWALK_IMAGE = pygame.image.load("./FormattedAssets/Sidewalk.png")
SIDEWALK_IMAGE = pygame.transform.scale(
    SIDEWALK_IMAGE, (GAME_CHUNK_SIZE, GAME_CHUNK_SIZE)
)
