import pygame
from constants import COLORS

class GameAssets:
    def __init__(self, screen_w, screen_h, cx, cy):
        self.BOARD_SCALE = 0.66
        self.board_size = int(min(screen_w, screen_h) * self.BOARD_SCALE)
        self.board_half = self.board_size // 2
        self.board_topleft = (cx - self.board_half, cy - self.board_half)
        
        self.background = self.load_asset("assets/background.png", screen_w, screen_h)
        
        frame_margin = int(self.board_size * 0.08)
        frame_size = self.board_size + frame_margin
        self.frame = self.load_asset("assets/frame.png", frame_size, frame_size)
        self.frame_topleft = (cx - self.frame.get_width() // 2, cy - self.frame.get_height() // 2)
        
        self.board_img = self.load_asset("assets/board.png", self.board_size, self.board_size)
    
    def load_asset(self, name, w, h):
        img = pygame.image.load(name).convert_alpha()
        return pygame.transform.smoothscale(img, (int(w), int(h)))
        