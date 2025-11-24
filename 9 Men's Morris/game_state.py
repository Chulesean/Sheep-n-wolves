import pygame

class GameState:
    def __init__(self, board_geometry):
        self.board = board_geometry
        self.occupied = [None] * 24
        self.turn = "W"
        self.placed = {"W": 0, "B": 0}
        self.capturing = False
        self.selected_piece = None
        self.phase = "placement"
        self.winner = None
        self.win_reason = ""
        self.FONT = pygame.font.SysFont(None, 40)
    
    def is_mill(self, pos, color):
        return any(all(self.occupied[p] == color for p in mill) 
                 for mill in self.board.mills if pos in mill)
    
    def count_pieces(self, color):
        return sum(1 for p in self.occupied if p == color)
    
    def player_can_fly(self, color):
        return self.count_pieces(color) == 3
    
    def valid_move(self, src, dst, mover_color):
        if self.occupied[src] != mover_color or self.occupied[dst] is not None:
            return False
        return self.player_can_fly(mover_color) or dst in self.board.adjacency[src]
    
    def has_any_valid_moves(self, color):
        if self.phase == "placement":
            return self.placed[color] < 9 and any(cell is None for cell in self.occupied)
        
        if self.player_can_fly(color):
            return any(cell is None for cell in self.occupied)
        else:
            for i in range(24):
                if self.occupied[i] == color:
                    for neighbor in self.board.adjacency[i]:
                        if self.occupied[neighbor] is None:
                            return True
            return False
    
    def check_win_conditions(self, current_player):
        opponent = "B" if current_player == "W" else "W"
    

        if self.phase == "moving" and self.count_pieces(opponent) < 3:
            self.winner = current_player
            self.win_reason = f"{'White' if current_player == 'W' else 'Black'} wins! Opponent has less than 3 pieces."
            return True
    
        if not self.has_any_valid_moves(opponent):
            self.winner = current_player
            self.win_reason = f"{'White' if current_player == 'W' else 'Black'} wins! Opponent has no valid moves."
            return True
    
        return False
    
    def switch_turn(self):
        self.turn = "B" if self.turn == "W" else "W"
        if self.placed["W"] == 9 and self.placed["B"] == 9:
            self.phase = "moving"
        
        if self.phase == "moving" and not self.has_any_valid_moves(self.turn):
            opponent = "B" if self.turn == "W" else "W"
            self.winner = opponent
            self.win_reason = f"{'White' if opponent == 'W' else 'Black'} wins! {('White' if self.turn == 'W' else 'Black')}."
