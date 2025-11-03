import pygame

# Màu sắc
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (220, 0, 0),
    'BLUE': (0, 0, 220),
    'GRAY': (180, 180, 180),
    'GREEN': (0, 180, 0)
}

#screen setup
def setup_screen():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_w, screen_h = screen.get_size()
    cx, cy = screen_w // 2, screen_h // 2
    pygame.display.set_caption("Nine Men's Morris")
    return screen, screen_w, screen_h, cx, cy