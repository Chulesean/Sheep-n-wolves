import pygame
from constants import COLORS

class GameAssets:
    def __init__(self, screen_w, screen_h, cx, cy):
        self.board_size = int(min(screen_w, screen_h) * 0.8)
        self.square_size = self.board_size // 8
        self.board_topleft = (cx - self.board_size // 2, cy - self.board_size // 2)
        
        self.background = self.create_background(screen_w, screen_h)
        
        frame_margin = int(self.board_size * 0.05)
        frame_size = self.board_size + frame_margin * 2
        self.frame = self.create_frame(frame_size, frame_size)
        self.frame_topleft = (cx - frame_size // 2, cy - frame_size // 2)
        
        self.board_img = self.create_board(self.board_size, self.board_size)
        
        piece_size = int(self.square_size * 0.7)
        self.white_piece_img = self.create_piece_image(piece_size, COLORS['WHITE'])
        self.black_piece_img = self.create_piece_image(piece_size, COLORS['BLACK'])
        self.white_king_img = self.create_king_image(piece_size, COLORS['WHITE'])
        self.black_king_img = self.create_king_image(piece_size, COLORS['BLACK'])
    
    def create_background(self, w, h):
        surface = pygame.Surface((w, h))
        for y in range(h):
            color_value = 50 + int(50 * (y / h))
            pygame.draw.line(surface, (color_value, color_value, color_value), (0, y), (w, y))
        return surface
    
    def create_frame(self, w, h):
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surface, (139, 69, 19, 200), (0, 0, w, h), border_radius=15)
        pygame.draw.rect(surface, (101, 67, 33), (0, 0, w, h), 5, border_radius=15)
        return surface
    
    def create_board(self, w, h):
        """Tạo hình ảnh bàn cờ"""
        surface = pygame.Surface((w, h))
        square_size = w // 8
        
        for row in range(8):
            for col in range(8):
                color = COLORS['DARK_BROWN'] if (row + col) % 2 == 1 else COLORS['LIGHT_BROWN']
                pygame.draw.rect(surface, color,
                               (col * square_size, row * square_size, square_size, square_size))
        
        for i in range(9):
            pygame.draw.line(surface, COLORS['BLACK'], (0, i * square_size), (w, i * square_size), 1)
            pygame.draw.line(surface, COLORS['BLACK'], (i * square_size, 0), (i * square_size, h), 1)
        
        return surface
    
    def create_piece_image(self, size, color):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        radius = size // 2 - 2
        center = (size // 2, size // 2)
        
        pygame.draw.circle(surface, (0, 0, 0, 100), (center[0]+2, center[1]+2), radius)
        
        pygame.draw.circle(surface, color, center, radius)
        pygame.draw.circle(surface, COLORS['BLACK'], center, radius, 2)
        
        return surface
    
    def create_king_image(self, size, color):
        """Tạo hình ảnh quân vua"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        radius = size // 2 - 2
        center = (size // 2, size // 2)
        
        pygame.draw.circle(surface, (0, 0, 0, 100), (center[0]+2, center[1]+2), radius)
        
        pygame.draw.circle(surface, color, center, radius)
        pygame.draw.circle(surface, COLORS['BLACK'], center, radius, 2)
        
        crown_color = COLORS['YELLOW']
        crown_size = radius // 2
        
        pygame.draw.circle(surface, crown_color, center, crown_size)
        pygame.draw.circle(surface, COLORS['BLACK'], center, crown_size, 1)
        
        font = pygame.font.SysFont(None, crown_size)
        text = font.render('K', True, COLORS['BLACK'])
        text_rect = text.get_rect(center=center)
        surface.blit(text, text_rect)
        
        return surface