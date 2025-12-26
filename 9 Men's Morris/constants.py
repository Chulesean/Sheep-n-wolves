"""
Constants module for Nine Men's Morris game.

Contains color definitions, screen setup, and game configurations.
All constants are defined here for centralized management.
"""

import pygame
from dataclasses import dataclass

# Color definitions
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (220, 0, 0),
    'BLUE': (0, 0, 220),
    'GRAY': (180, 180, 180),
    'GREEN': (0, 180, 0)
}

# ===== ASSET SCALING CONSTANTS =====
BOARD_SCALE = 0.66          # Board takes 66% of smaller screen dimension
FRAME_MARGIN_SCALE = 0.08   # Frame extends 8% beyond board edges
PIECE_SCALE = 0.06          # Piece size is 6% of board size

# ===== GAME CONFIGURATIONS =====
BOT_COLOR = "B"            # Bot always plays as Black
PLAYER_COLOR = "W"         # Player always plays as White

# ===== BOT SETTINGS =====
BOT_DELAY = 1.0            # Delay between bot moves in seconds
BOT_TIMEOUT = 3.0          # Maximum time bot can think (defined for future use)

# ===== GAME RETURN STATUS =====
RETURN_TO_MENU = 0
QUIT_GAME = 1

@dataclass
class ScreenConfig:
    """Container for screen configuration."""
    screen: pygame.Surface
    width: int
    height: int
    center_x: int
    center_y: int

def setup_screen() -> ScreenConfig:
    """Initialize screen and return configuration."""
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_w, screen_h = screen.get_size()
    cx, cy = screen_w // 2, screen_h // 2
    pygame.display.set_caption("Nine Men's Morris")
    return ScreenConfig(screen, screen_w, screen_h, cx, cy)
