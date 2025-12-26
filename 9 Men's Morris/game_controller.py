"""
Input handling and bot control for Nine Men's Morris.

Processes player clicks, validates moves, manages bot AI decisions,
and coordinates game flow between state and user interactions.
"""

import random
import pygame
from bot import NineMensMorrisBot
from constants import BOT_COLOR, PLAYER_COLOR, BOT_DELAY
import time

class GameController:
    """Handles game input and bot control."""
    
    def __init__(self, board_geometry, game_state):
        self.board = board_geometry
        self.state = game_state
        self.bot = None
        self.vs_bot = False
        self.last_bot_move_time = 0
        self.bot_delay = BOT_DELAY  # Use constant
        self.bot_thinking = False
        self.bot_color = BOT_COLOR
        self.player_color = PLAYER_COLOR

    def set_vs_bot(self, enabled):
        """Enable or disable bot opponent."""
        self.vs_bot = enabled
        if enabled:
            self.bot = NineMensMorrisBot()

    def nearest_point(self, mouse_pos):
        """Find nearest board point to mouse position."""
        for i, point in enumerate(self.board.points):
            if self.distance(mouse_pos, point) < 25:
                return i
        return None

    def distance(self, pos1, pos2):
        """Calculate Euclidean distance."""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def handle_click(self, idx):
        """Handle mouse click on board."""
        if self.state.winner or self.bot_thinking:
            return

        # Check if it's bot's turn (when playing vs bot)
        if self.vs_bot and self.state.turn == self.bot_color:
            return

        mover = self.state.turn
        opponent = self.bot_color if mover == self.player_color else self.player_color

        if self.state.capturing:
            self.handle_capture(idx, mover, opponent)
        elif self.state.phase == "placement":
            self.handle_placement(idx, mover)
        else:
            self.handle_movement(idx, mover)

    def handle_capture(self, idx, mover, opponent):
        """Handle capture action."""
        if self.state.occupied[idx] == opponent:
            opponent_pieces = [p for p in range(self.board.TOTAL_POINTS) if self.state.occupied[p] == opponent]
            non_mill_pieces = [p for p in opponent_pieces if not self.state.is_mill(p, opponent)]

            # Only allow capturing non-mill pieces if available
            if non_mill_pieces and self.state.is_mill(idx, opponent):
                return  # Cannot capture piece in mill when other pieces available
                
            self.state.occupied[idx] = None
            self.state.capturing = False
            self.state.selected_piece = None

            if self.state.phase == "moving":
                self.state.check_win_conditions(mover)
                if not self.state.winner:
                    self.state.switch_turn()
            else:
                self.state.switch_turn()

    def handle_placement(self, idx, mover):
        """Handle piece placement during placement phase."""
        # Use game state method to validate
        if self.state.is_valid_placement(idx, mover):
            self.state.place_piece(idx, mover)
        else:
            print(f"[INFO] Invalid placement at {idx}")
    
    def handle_movement(self, idx, mover):
        """Handle piece movement during moving phase."""
        if self.state.selected_piece is None:
            if self.state.occupied[idx] == mover:
                self.state.selected_piece = idx
        else:
            # Use game state method to validate
            if self.state.is_valid_move(self.state.selected_piece, idx, mover):
                self.state.move_piece(self.state.selected_piece, idx, mover)
                self.state.selected_piece = None
            elif self.state.occupied[idx] == mover:
                self.state.selected_piece = idx

    def update(self):
        """Update game state (called every frame)."""
        if self.state.winner:
            return

        current_time = time.time()
        
        # Bot's turn (only when vs bot and bot's turn)
        if (self.vs_bot and self.state.turn == self.bot_color and self.bot and 
            current_time - self.last_bot_move_time >= self.bot_delay and
            not self.bot_thinking):
            
            self.bot_thinking = True
            
            try:
                if self.state.capturing:
                    capture_move = self.get_bot_capture_move()
                    if capture_move is not None:
                        self.execute_bot_capture(capture_move)
                    else:
                        self.state.capturing = False
                        self.state.switch_turn()
                else:
                    move = self.bot.get_move(self.state)
                    if move:
                        self.execute_bot_move(move)
                    else:
                        self.state.switch_turn()
                        
            except Exception as e:
                print(f"Bot error: {e}")
                self.state.capturing = False
                self.state.switch_turn()
            
            finally:
                self.last_bot_move_time = current_time
                self.bot_thinking = False

    def get_bot_capture_move(self):
        """Bot choosing an opponent's piece for capture."""
        try:
            opponent_color = self.player_color  # Bot captures player's pieces
            opponent_pieces = [p for p in range(self.board.TOTAL_POINTS) 
                             if self.state.occupied[p] == opponent_color]
            
            if not opponent_pieces:
                return None
            
            non_mill_pieces = [p for p in opponent_pieces 
                             if not self.state.is_mill(p, opponent_color)]
            
            if non_mill_pieces:
                return random.choice(non_mill_pieces)
            else:
                return random.choice(opponent_pieces)
                
        except Exception as e:
            print(f"Error in get_bot_capture_move: {e}")
            return None

    def execute_bot_capture(self, target_pos):
        """Execute bot capture move."""
        try:
            opponent_color = self.player_color
            
            # Validate using game state
            if (0 <= target_pos < self.board.TOTAL_POINTS and 
                self.state.occupied[target_pos] == opponent_color and
                not (self.has_non_mill_pieces(opponent_color) and 
                     self.state.is_mill(target_pos, opponent_color))):
                
                self.state.occupied[target_pos] = None
                self.state.capturing = False
            
                if self.state.phase == "moving":
                    self.state.check_win_conditions(self.bot_color)
                    if not self.state.winner:
                        self.state.switch_turn()
                else:
                    self.state.switch_turn()
            else:
                # If capture is invalid, switch turn
                self.state.capturing = False
                self.state.switch_turn()
                    
        except Exception as e:
            print(f"Error in execute_bot_capture: {e}")
            self.state.capturing = False
            self.state.switch_turn()

    def execute_bot_move(self, move):
        """Execute bot placement or movement move using game state methods."""
        try:
            if self.state.phase == "placement":
                # Use game state method to validate
                if isinstance(move, int) and self.state.is_valid_placement(move, self.bot_color):
                    success = self.state.place_piece(move, self.bot_color)
                    if not success:
                        print(f"[WARN] Bot placement failed at position {move}")
                        self.state.switch_turn()
                else:
                    print(f"[WARN] Bot placement invalid: {move}")
                    self.state.switch_turn()
                        
            else:  # moving phase
                # Use game state method to validate
                if isinstance(move, tuple) and len(move) == 2:
                    src, dst = move
                    if self.state.is_valid_move(src, dst, self.bot_color):
                        success = self.state.move_piece(src, dst, self.bot_color)
                        if not success:
                            print(f"[WARN] Bot move failed: {src}->{dst}")
                            self.state.switch_turn()
                    else:
                        print(f"[WARN] Bot move invalid: {src}->{dst}")
                        self.state.switch_turn()
                            
        except Exception as e:
            print(f"Error in execute_bot_move: {e}")
            self.state.capturing = False
            self.state.switch_turn()
    
    def has_non_mill_pieces(self, color):
        """Check if player has any pieces not in mills."""
        pieces = [p for p in range(self.board.TOTAL_POINTS) if self.state.occupied[p] == color]
        non_mill_pieces = [p for p in pieces if not self.state.is_mill(p, color)]
        return len(non_mill_pieces) > 0
    
