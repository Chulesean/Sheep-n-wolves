import pygame
from constants import COLORS

class GameRenderer:
    def __init__(self, assets, board, game_state, screen, screen_w, screen_h):
        self.assets = assets
        self.board = board
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
        self.screen.blit(self.assets.board_img, self.assets.board_topleft)
        self._draw_must_capture_highlight()

    def _draw_must_capture_highlight(self):
       
        if not self.state.must_capture:
            return
        
        square_size = self.assets.square_size
        board_left, board_top = self.assets.board_topleft
        
        pieces = self.board.get_all_pieces(self.state.turn)
        
        for piece in pieces:

            moves = self.board.get_valid_moves(piece)
            if any(captured for captured in moves.values()):
                
                x = board_left + piece.col * square_size
                y = board_top + piece.row * square_size
                

                s = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                s.fill((0, 255, 0, 60))
                self.screen.blit(s, (x, y))
    def draw_pieces(self):
        square_size = self.assets.square_size
        board_left, board_top = self.assets.board_topleft
        
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece:
                    x = board_left + col * square_size + square_size // 2
                    y = board_top + row * square_size + square_size // 2
                    
                    if piece.color == 'white':
                        img = self.assets.white_king_img if piece.king else self.assets.white_piece_img
                    else:
                        img = self.assets.black_king_img if piece.king else self.assets.black_piece_img
                    
                    img_rect = img.get_rect(center=(x, y))
                    self.screen.blit(img, img_rect)
                    
                    if piece.selected:
                        pygame.draw.circle(self.screen, COLORS['GREEN'], (x, y), 
                                          square_size // 2 - 5, 3)
    
    def draw_valid_moves(self):
        if not self.state.selected:
            return
        
        square_size = self.assets.square_size
        board_left, board_top = self.assets.board_topleft
        
        for (row, col), captured in self.state.valid_moves.items():
            x = board_left + col * square_size + square_size // 2
            y = board_top + row * square_size + square_size // 2
            
            s = pygame.Surface((square_size - 10, square_size - 10), pygame.SRCALPHA)
            
            if captured:
                s.fill(COLORS['CAPTURE_HIGHLIGHT'])
                font = pygame.font.SysFont(None, 24)
                text = font.render(f'{len(captured)}', True, COLORS['WHITE'])
                text_rect = text.get_rect(center=(square_size//2 - 5, square_size//2 - 5))
                s.blit(text, text_rect)
            else:
                s.fill(COLORS['MOVE_HIGHLIGHT'])
            
            self.screen.blit(s, (board_left + col * square_size + 5, 
                               board_top + row * square_size + 5))
    
    def draw_ui(self):
        info_height = 60
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (0, 0, self.screen_w, info_height))
        
        turn_color = COLORS['WHITE'] if self.state.turn == 'white' else COLORS['BLACK']
        turn_text = f"Turn: {'WHITE' if self.state.turn == 'white' else 'BLACK'}"
        text_surface = self.state.FONT.render(turn_text, True, turn_color)
        self.screen.blit(text_surface, (20, 10))
        
        white_text = f"WHITE: {self.board.white_left}"
        black_text = f"BLACK: {self.board.black_left}"
        
        white_surf = self.state.FONT.render(white_text, True, COLORS['WHITE'])
        black_surf = self.state.FONT.render(black_text, True, COLORS['BLACK'])
        
        self.screen.blit(white_surf, (self.screen_w - 150, 10))
        self.screen.blit(black_surf, (self.screen_w - 150, 40))
        
        if self.state.must_capture:
            warning_font = pygame.font.SysFont(None, 32)
            warning = warning_font.render("CAPTURE MANDATORY", True, COLORS['RED'])
            self.screen.blit(warning, (self.screen_w // 2 - 100, 10))
        
        if self.state.game_over:
            self.draw_game_over()
    
    def draw_game_over(self):
        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.SysFont(None, 72)
        font_medium = pygame.font.SysFont(None, 36)
        
        winner_text = f"{'WHITE' if self.state.winner == 'white' else 'BLACK'} WINS!"
        winner_color = COLORS['WHITE'] if self.state.winner == 'white' else COLORS['BLACK']
        
        text = font_large.render(winner_text, True, winner_color)
        text_rect = text.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 50))
        self.screen.blit(text, text_rect)
        
        if self.state.winner == 'white':
            reason_text = "White's out of moves!"
        else:
            reason_text = "Black's out of moves!"
        
        reason = font_medium.render(reason_text, True, COLORS['WHITE'])
        reason_rect = reason.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 20))
        self.screen.blit(reason, reason_rect)
       
        restart_text = font_medium.render("Press ESC to exit", True, COLORS['WHITE'])
        restart_rect = restart_text.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 80))
        self.screen.blit(restart_text, restart_rect)