"""
AI opponent for Nine Men's Morris.

Implements computer player logic for both placement and movement phases.
Prioritizes mill creation and follows game rules including flying when applicable.
"""

import random
from constants import BOT_COLOR, PLAYER_COLOR

class NineMensMorrisBot:
    """
    AI bot that plays Nine Men's Morris as the Black player.
    
    Strategy:
    1. During placement: First tries to create mills, otherwise places randomly
    2. During movement: First tries to create mills, otherwise moves randomly
    3. Follows flying rule when piece count drops to 3
    """
    
    def __init__(self):
        """Initialize bot."""
        self.bot_color = BOT_COLOR
        self.player_color = PLAYER_COLOR
    
    def get_move(self, game_state):
        """
        Get bot's next move based on current game state.
        
        Args:
            game_state (GameState): Current game state
            
        Returns:
            Placement: int position index
            Movement: (src, dst) tuple
            None: If no valid move
        """
        if game_state.phase == "placement":
            return self.get_placement_move(game_state)
        else:
            return self.get_movement_move(game_state)
    
    def get_placement_move(self, game_state):
        """Get placement move during placement phase."""
        if game_state.placed[self.bot_color] >= 9:
            return None
            
        empty_positions = [i for i, occ in enumerate(game_state.occupied) if occ is None]
        if not empty_positions:
            return None
        
        for pos in empty_positions:
            if self.would_create_mill(game_state, pos, self.bot_color):
                return pos
        
        return random.choice(empty_positions)
    
    def get_movement_move(self, game_state):
        """Get movement move during movement phase."""
        bot_pieces = [i for i, occ in enumerate(game_state.occupied) if occ == self.bot_color]
        
        if not bot_pieces:
            return None
        
        for src in bot_pieces:
            possible_moves = self.get_possible_moves(game_state, src)
            for dst in possible_moves:
                if self.would_create_mill(game_state, dst, self.bot_color):
                    return (src, dst)
        
        return self.get_random_move(game_state)
    
    def get_random_move(self, game_state):
        """Get random valid move when no mill-creating move is available."""
        bot_pieces = [i for i, occ in enumerate(game_state.occupied) if occ == self.bot_color]
        
        if not bot_pieces:
            return None
            
        random.shuffle(bot_pieces)
        
        for src in bot_pieces:
            possible_moves = self.get_possible_moves(game_state, src)
            if possible_moves:
                return (src, random.choice(possible_moves))
        
        return None
    
    def get_possible_moves(self, game_state, src):
        """Get all possible destination positions from source."""
        if game_state.player_can_fly(self.bot_color):
            return [i for i, occ in enumerate(game_state.occupied) if occ is None]
        else:
            return [dst for dst in game_state.board.adjacency[src] if game_state.occupied[dst] is None]
    
    def would_create_mill(self, game_state, position, color):
        """Check if placing/moving to position would create a mill."""
        original = game_state.occupied[position]
        game_state.occupied[position] = color
        creates_mill = game_state.is_mill(position, color)
        game_state.occupied[position] = original
        return creates_mill
    
