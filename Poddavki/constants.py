import pygame

# Color definitions used throughout the game
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (220, 0, 0),
    'BLUE': (0, 120, 220),
    'GREEN': (0, 180, 0),
    'YELLOW': (255, 215, 0),
    'DARK_BROWN': (101, 67, 33),
    'LIGHT_BROWN': (210, 180, 140),
    'GRAY': (180, 180, 180),
    'HIGHLIGHT': (255, 255, 0, 128),
    'MOVE_HIGHLIGHT': (0, 255, 0, 100),
    'CAPTURE_HIGHLIGHT': (255, 0, 0, 100)
}

# Board dimensions
ROWS, COLS = 8, 8


def setup_screen(fullscreen=False):
    """
    Initialize the game window and configure display settings.

    :param fullscreen: Whether to start the game in fullscreen mode
    :return: Tuple containing:
             - screen: Pygame display surface
             - screen_w: Screen width
             - screen_h: Screen height
             - cx: X coordinate of screen center
             - cy: Y coordinate of screen center
    """
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 850))

    screen_w, screen_h = screen.get_size()
    cx, cy = screen_w // 2, screen_h // 2

    pygame.display.set_caption("Poddavki Checkers")

    return screen, screen_w, screen_h, cx, cy
