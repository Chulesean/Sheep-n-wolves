"""
Visual rendering for Nine Men's Morris.

Draws game board, pieces, UI elements, and visual effects.
Handles blinking indicators for available positions during placement phase.
"""

import pygame
from constants import COLORS

class GameRenderer:
    """
    Renderer class for displaying all game visuals.
    
    Handles drawing of board, pieces, UI elements, and visual effects.
    Manages blinking indicators for available moves during placement phase.
    """
    
    def __init__(self, assets, board_geometry, game_state, screen, screen_w, screen_h):
        """
        Initialize game renderer.
        
        Args:
            assets (GameAssets): Game assets instance
            board_geometry (BoardGeometry): Board geometry instance
            game_state (GameState): Current game state
            screen (pygame.Surface): Display surface
            screen_w (int): Screen width
            screen_h (int): Screen height
        """
        self.assets = assets
        self.board = board_geometry
        self.state = game_state
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.blink_timer = 0
        
        # Cache for text surfaces to improve performance
        self.cached_text = {
            'piece_count': {'W': None, 'B': None, 'white_left': 9, 'black_left': 9},
            'turn_label': {'text': '', 'surface': None},
            'capture_msg': {'text': '', 'surface': None}
        }
    
    def draw_background(self):
        """Draw game background image."""
        self.screen.blit(self.assets.background, (0, 0))
    
    def draw_frame(self):
        """Draw decorative frame around game board."""
        self.screen.blit(self.assets.frame, self.assets.frame_topleft)
    
    def draw_board(self):
        """Draw game board with connections and points."""
        self.screen.blit(self.assets.board_img, self.assets.board_topleft)
        for a, b in self.board.connections:
            pygame.draw.line(self.screen, COLORS['BLACK'], self.board.points[a], self.board.points[b], 3)
        for point in self.board.points:
            pygame.draw.circle(self.screen, COLORS['BLACK'], point, 6)
    
    def draw_pieces(self):
        """Draw all game pieces on the board."""
        for i, occ in enumerate(self.state.occupied):
            x, y = self.board.points[i]
            if occ == "W":
                # GameAssets ensures valid surface
                img_rect = self.assets.white_piece_img.get_rect(center=(x, y))
                self.screen.blit(self.assets.white_piece_img, img_rect)
            elif occ == "B":
                # GameAssets ensures valid surface
                img_rect = self.assets.black_piece_img.get_rect(center=(x, y))
                self.screen.blit(self.assets.black_piece_img, img_rect)
        
        if self.state.selected_piece is not None:
            x, y = self.board.points[self.state.selected_piece]
            pygame.draw.circle(self.screen, COLORS['RED'], (x, y), 22, 3)
    
    def draw_available_positions(self):
        """Draw blinking indicators for available positions during placement phase."""
        if self.state.phase != "placement" or self.state.winner:
            return
        
        self.blink_timer = (self.blink_timer + 1) % 120
        is_visible = self.blink_timer < 60
        
        if is_visible:
            blink_color = COLORS['GREEN']
            for i, point in enumerate(self.board.points):
                if self.state.occupied[i] is None:
                    pygame.draw.circle(self.screen, blink_color, point, 8)
    
    def draw_ui(self):
        """Draw user interface elements."""
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
        
        # Draw current turn label (with caching)
        player_name = "White" if self.state.turn == "W" else "Black"
        turn_label = f"{player_name}'s turn | Phase: {self.state.phase}"
        
        # Check if we need to re-render
        if (self.cached_text['turn_label']['text'] != turn_label or 
            self.cached_text['turn_label']['surface'] is None):
            
            color = COLORS['RED'] if self.state.turn == "B" else COLORS['BLUE']
            self.cached_text['turn_label']['surface'] = self.state.FONT.render(turn_label, True, color)
            self.cached_text['turn_label']['text'] = turn_label
        
        text_rect = self.cached_text['turn_label']['surface'].get_rect(center=(self.screen_w // 2, 40))
        self.screen.blit(self.cached_text['turn_label']['surface'], text_rect)
        
        # Draw capture message (with caching)
        if self.state.capturing:
            capture_msg = "Capture any opponent's piece!"
            
            # Check if we need to re-render
            if (self.cached_text['capture_msg']['text'] != capture_msg or 
                self.cached_text['capture_msg']['surface'] is None):
                
                self.cached_text['capture_msg']['surface'] = self.state.FONT.render(capture_msg, True, COLORS['RED'])
                self.cached_text['capture_msg']['text'] = capture_msg
            
            capture_rect = self.cached_text['capture_msg']['surface'].get_rect(center=(self.screen_w // 2, 80))
            self.screen.blit(self.cached_text['capture_msg']['surface'], capture_rect)
        else:
            # Clear cache if not capturing
            self.cached_text['capture_msg']['text'] = ''
            self.cached_text['capture_msg']['surface'] = None
        
        # Draw remaining pieces during placement phase (with caching)
        if self.state.phase == "placement":
            white_left = 9 - self.state.placed["W"]
            black_left = 9 - self.state.placed["B"]
            
            # Check if we need to re-render white pieces text
            if (self.cached_text['piece_count']['white_left'] != white_left or 
                self.cached_text['piece_count']['W'] is None):
                
                white_text = f"White pieces left: {white_left}"
                self.cached_text['piece_count']['W'] = self.state.FONT.render(white_text, True, COLORS['WHITE'])
                self.cached_text['piece_count']['white_left'] = white_left
            
            # Check if we need to re-render black pieces text
            if (self.cached_text['piece_count']['black_left'] != black_left or 
                self.cached_text['piece_count']['B'] is None):
                
                black_text = f"Black pieces left: {black_left}"
                self.cached_text['piece_count']['B'] = self.state.FONT.render(black_text, True, COLORS['BLACK'])
                self.cached_text['piece_count']['black_left'] = black_left
            
            # Use relative positioning for responsiveness
            y_offset = self.screen_h - 100  # 100px from bottom
            white_rect = self.cached_text['piece_count']['W'].get_rect(
                midleft=(int(self.screen_w * 0.05), y_offset)
            )
            black_rect = self.cached_text['piece_count']['B'].get_rect(
                midright=(int(self.screen_w * 0.95), y_offset)
            )
            
            self.screen.blit(self.cached_text['piece_count']['W'], white_rect)
            self.screen.blit(self.cached_text['piece_count']['B'], black_rect)
        else:
            # Clear cache if not in placement phase
            self.cached_text['piece_count']['W'] = None
            self.cached_text['piece_count']['B'] = None
            self.cached_text['piece_count']['white_left'] = 9
            self.cached_text['piece_count']['black_left'] = 9
            
