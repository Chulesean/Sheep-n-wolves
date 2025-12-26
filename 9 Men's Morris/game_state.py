"""
Game state management for Nine Men's Morris.

Tracks board occupancy, current turn, game phase, mills, and win conditions.
Contains logic for move validation and piece counting.
"""

import pygame

class GameState:
    """Manages the state of the Nine Men's Morris game."""
    
    def __init__(self, board_geometry):
        self.board = board_geometry
        self.occupied = [None] * board_geometry.TOTAL_POINTS
        self.turn = "W"
        self.placed = {"W": 0, "B": 0}
        self.capturing = False
        self.selected_piece = None
        self.phase = "placement"
        self.winner = None
        self.win_reason = ""
        self.FONT = pygame.font.SysFont(None, 40)
      
    def is_valid_placement(self, position, color=None):
        """Check if placement is valid."""
        if color is None:
            color = self.turn
            
        if self.phase != "placement":
            return False
        if self.placed[color] >= 9:
            return False
        if not (0 <= position < self.board.TOTAL_POINTS):
            return False
        if self.occupied[position] is not None:
            return False
        return True
    
    def place_piece(self, position, color=None):
        """Place a piece on the board."""
        if color is None:
            color = self.turn
            
        if not self.is_valid_placement(position, color):
            return False
            
        self.occupied[position] = color
        self.placed[color] += 1
        
        if self.is_mill(position, color):
            self.capturing = True
        else:
            self.switch_turn()
            
        return True
    
    def is_valid_move(self, src, dst, color=None):
        """Check if move is valid."""
        if color is None:
            color = self.turn
            
        if self.phase != "moving":
            return False
        if not (0 <= src < self.board.TOTAL_POINTS and 0 <= dst < self.board.TOTAL_POINTS):
            return False
        if self.occupied[src] != color:
            return False
        if self.occupied[dst] is not None:
            return False
        return self.valid_move(src, dst, color)
    
    def move_piece(self, src, dst, color=None):
        """Move a piece on the board."""
        if color is None:
            color = self.turn
            
        if not self.is_valid_move(src, dst, color):
            return False
            
        self.occupied[dst] = color
        self.occupied[src] = None
        
        if self.is_mill(dst, color):
            self.capturing = True
        else:
            self.switch_turn()
            
        return True
    
    def is_mill(self, pos, color):
        """Check if position forms a mill."""
        return any(all(self.occupied[p] == color for p in mill) 
                 for mill in self.board.mills if pos in mill)
    
    def count_pieces(self, color):
        """Count pieces of a given color."""
        return sum(1 for p in self.occupied if p == color)
    
    def player_can_fly(self, color):
        """Check if player can fly (has only 3 pieces)."""
        return self.count_pieces(color) == 3
    
    def valid_move(self, src, dst, mover_color):
        """Check if move is geometrically valid."""
        if self.occupied[src] != mover_color or self.occupied[dst] is not None:
            return False
        return self.player_can_fly(mover_color) or dst in self.board.adjacency[src]
    
    def has_any_valid_moves(self, color):
        """Check if player has any valid moves."""
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
        """Check if current player has won."""
        opponent = "B" if current_player == "W" else "W"
    
        # Win condition 1: Opponent has less than 3 pieces
        if self.phase == "moving" and self.count_pieces(opponent) < 3:
            self.winner = current_player
            self.win_reason = f"{'White' if current_player == 'W' else 'Black'} wins! Opponent has less than 3 pieces."
            return True
    
        # Win condition 2: Opponent has no valid moves
        if not self.has_any_valid_moves(opponent):
            self.winner = current_player
            self.win_reason = f"{'White' if current_player == 'W' else 'Black'} wins! Opponent has no valid moves."
            return True
    
        return False
    
    def switch_turn(self):
        """Switch to the other player's turn."""
        # Switch to the other player
        self.turn = "B" if self.turn == "W" else "W"
        
        # Check if we should transition to moving phase
        if self.placed["W"] == 9 and self.placed["B"] == 9:
            self.phase = "moving"
        
        # After switching turns, check if the current player has won
        if self.phase == "moving" and not self.winner:
            self.check_win_conditions(self.turn)
            
