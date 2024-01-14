import pygame
import sys
from wordle import WordleGame

pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
FONT = pygame.font.Font(OPEN_SANS, 36)
