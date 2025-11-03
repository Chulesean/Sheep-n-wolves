import pygame
from constants import COLORS

class GameRenderer:
    def __init__(self, assets, board_geometry, game_state, screen, screen_w, screen_h):
        self.assets = assets
        self.board = board_geometry
        self.state = game_state
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
    
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
            if occ == "W":
                pygame.draw.circle(self.screen, COLORS['WHITE'], self.board.points[i], 18)
                pygame.draw.circle(self.screen, COLORS['BLACK'], self.board.points[i], 18, 2)
            elif occ == "B":
                pygame.draw.circle(self.screen, COLORS['BLACK'], self.board.points[i], 18)
        
        if self.state.selected_piece is not None:
            pygame.draw.circle(self.screen, COLORS['RED'], self.board.points[self.state.selected_piece], 22, 3)
    
    def draw_ui(self):
        if self.state.winner:
            self.screen.blit(self.state.FONT.render(self.state.win_reason, True, COLORS['GREEN']), (1000, 20))
            return
        
        label = f"{'White' if self.state.turn == 'W' else 'Black'}'s turn | Phase: {self.state.phase}"
        color = COLORS['RED'] if self.state.turn == "B" else COLORS['BLUE']
        self.screen.blit(self.state.FONT.render(label, True, color), (20, 20))
        
        if self.state.capturing:
            self.screen.blit(self.state.FONT.render("Capture any opponent's piece!", True, COLORS['RED']), (20, 60))
        
        if self.state.phase == "placement":
            white_left = 9 - self.state.placed["W"]
            black_left = 9 - self.state.placed["B"]
            
            self.screen.blit(self.state.FONT.render(f"White pieces left: {white_left}", True, COLORS['WHITE']), (150, self.screen_h // 2 - 20))
            self.screen.blit(self.state.FONT.render(f"Black pieces left: {black_left}", True, COLORS['BLACK']), (self.screen_w - 500, self.screen_h // 2 - 20))