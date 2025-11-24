import random

class NineMensMorrisBot:
    def __init__(self, difficulty="EASY"):
        self.difficulty = difficulty
    
    def get_move(self, game_state):
        if game_state.phase == "placement":
            return self.get_placement_move(game_state)
        else:
            return self.get_movement_move(game_state)
    
    def get_placement_move(self, game_state):
        if game_state.placed["B"] >= 9:
            return None
            
        empty_positions = [i for i, occ in enumerate(game_state.occupied) if occ is None]
        if not empty_positions:
            return None
        
        for pos in empty_positions:
            if self.would_create_mill(game_state, pos, "B"):
                return pos
        
        return random.choice(empty_positions)
    
    def get_movement_move(self, game_state):
        bot_pieces = [i for i, occ in enumerate(game_state.occupied) if occ == "B"]
        
        if not bot_pieces:
            return None
        
        for src in bot_pieces:
            possible_moves = self.get_possible_moves(game_state, src)
            for dst in possible_moves:
                if self.would_create_mill(game_state, dst, "B"):
                    return (src, dst)
        
        return self.get_random_move(game_state)
    
    def get_random_move(self, game_state):
        bot_pieces = [i for i, occ in enumerate(game_state.occupied) if occ == "B"]
        
        if not bot_pieces:
            return None
            
        random.shuffle(bot_pieces)
        
        for src in bot_pieces:
            possible_moves = self.get_possible_moves(game_state, src)
            if possible_moves:
                return (src, random.choice(possible_moves))
        
        return None
    
    def get_possible_moves(self, game_state, src):
        if game_state.player_can_fly("B"):
            return [i for i, occ in enumerate(game_state.occupied) if occ is None]
        else:
            return [dst for dst in game_state.board.adjacency[src] if game_state.occupied[dst] is None]
    
    def would_create_mill(self, game_state, position, color):
        original = game_state.occupied[position]
        game_state.occupied[position] = color
        creates_mill = game_state.is_mill(position, color)
        game_state.occupied[position] = original
        return creates_mill