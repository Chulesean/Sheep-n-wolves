import pygame

class GameController:
    def __init__(self, assets=None, board=None, game_state=None):
        self.assets = assets
        self.board = board
        self.state = game_state
        self.vs_bot = False
    
    def set_vs_bot(self, enabled):
        self.vs_bot = enabled
    
    def get_clicked_position(self, mouse_pos):
        if not self.assets:
            return None, None
            
        board_left, board_top = self.assets.board_topleft
        square_size = self.assets.square_size
        
        x, y = mouse_pos
        
        if (board_left <= x < board_left + 8 * square_size and
            board_top <= y < board_top + 8 * square_size):
            
            col = (x - board_left) // square_size
            row = (y - board_top) // square_size
            
            return row, col
        
        return None, None
    
    def handle_click(self, mouse_pos):
        if not self.state or self.state.game_over:
            return
        
        row, col = self.get_clicked_position(mouse_pos)
        if row is not None and col is not None:
            self.state.select(row, col)
    
    def handle_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            return 'exit'
        elif event.key == pygame.K_r:
            if self.state:
                self.state.reset()
            return 'reset'
        return None