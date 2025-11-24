import pygame
from constants import COLORS
import time

class GameRenderer:
    def __init__(self, assets, board_geometry, game_state, screen, screen_w, screen_h):
        self.assets = assets
        self.board = board_geometry
        self.state = game_state
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.blink_timer = 0
    
    def draw_background(self):
        self.screen.blit(self.assets.background, (0, 0))
    
    def draw_frame(self):
        self.screen.blit(self.assets.frame, self.assets.frame_topleft)
    
    def draw_board(self):
        self.screen.blit(self.assets.board_img, self.assets.board_topleft)
        for a, b in self.board.connections:
            pygame.draw.line(self.screen, COLORS['BLACK'], self.board.points[a], self.board.points[b], 3)
        for point in self.board.points:
            pygame.draw.circle(self.screen, COLORS['BLACK'], point, 6)
    
    def draw_pieces(self):
        for i, occ in enumerate(self.state.occupied):
            x, y = self.board.points[i]
            if occ == "W":
                if self.assets.white_piece_img:
                    img_rect = self.assets.white_piece_img.get_rect(center=(x, y))
                    self.screen.blit(self.assets.white_piece_img, img_rect)
                else:
                    pygame.draw.circle(self.screen, COLORS['WHITE'], (x, y), 18)
                    pygame.draw.circle(self.screen, COLORS['BLACK'], (x, y), 18, 2)
            elif occ == "B":
                if self.assets.black_piece_img:
                    img_rect = self.assets.black_piece_img.get_rect(center=(x, y))
                    self.screen.blit(self.assets.black_piece_img, img_rect)
                else:
                    pygame.draw.circle(self.screen, COLORS['BLACK'], (x, y), 18)
        
        if self.state.selected_piece is not None:
            x, y = self.board.points[self.state.selected_piece]
            pygame.draw.circle(self.screen, COLORS['RED'], (x, y), 22, 3)
    
    def draw_available_positions(self):
        if self.state.phase != "placement" or self.state.winner:
            return
        
        # NHẤP NHÁY CHẬM (2 giây)
        self.blink_timer = (self.blink_timer + 1) % 120
        is_visible = self.blink_timer < 60
        
        if is_visible:
            blink_color = COLORS['GREEN']
            for i, point in enumerate(self.board.points):
                if self.state.occupied[i] is None:
                    pygame.draw.circle(self.screen, blink_color, point, 8)
    
    def draw_ui(self):
        if self.state.winner:
            msg = self.state.win_reason
            text_surface = self.state.FONT.render(msg, True, COLORS['GREEN'])
            text_rect = text_surface.get_rect(center=(self.screen_w // 2, 50))
            self.screen.blit(text_surface, text_rect)
            
            exit_msg = "Press ESC to exit"
            exit_surface = self.state.FONT.render(exit_msg, True, COLORS['RED'])
            exit_rect = exit_surface.get_rect(center=(self.screen_w // 2, 90))
            self.screen.blit(exit_surface, exit_rect)
            return
        
        player_name = "White" if self.state.turn == "W" else "Black"
        label = f"{player_name}'s turn | Phase: {self.state.phase}"
        color = COLORS['RED'] if self.state.turn == "B" else COLORS['BLUE']
        
        text_surface = self.state.FONT.render(label, True, color)
        text_rect = text_surface.get_rect(center=(self.screen_w // 2, 40))
        self.screen.blit(text_surface, text_rect)
        
        if self.state.capturing:
            capture_msg = "Capture any opponent's piece!"
            capture_surface = self.state.FONT.render(capture_msg, True, COLORS['RED'])
            capture_rect = capture_surface.get_rect(center=(self.screen_w // 2, 80))
            self.screen.blit(capture_surface, capture_rect)
        
        if self.state.phase == "placement":
            white_left = 9 - self.state.placed["W"]
            black_left = 9 - self.state.placed["B"]
            
            white_text = f"White pieces left: {white_left}"
            black_text = f"Black pieces left: {black_left}"
            
            white_surface = self.state.FONT.render(white_text, True, COLORS['WHITE'])
            black_surface = self.state.FONT.render(black_text, True, COLORS['BLACK'])
            
            white_rect = white_surface.get_rect(midleft=(50, self.screen_h - 500))
            black_rect = black_surface.get_rect(midright=(self.screen_w - 50, self.screen_h - 500))
            
            self.screen.blit(white_surface, white_rect)
            self.screen.blit(black_surface, black_rect)
