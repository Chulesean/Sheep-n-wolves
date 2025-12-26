"""
AI opponent for Poddavki Checkers (Russian Give-away Checkers).
The bot uses a "suicide" strategy - tries to lose pieces and avoid winning.
"""

import random

class PoddavkiBot:
    """AI bot that tries to lose by making bad moves."""
    
    def __init__(self, difficulty="SUICIDE"):
        self.difficulty = difficulty
        self.sacrifice_mode = False
    
    def get_move(self, game_state):
        """Get bot's next move."""
        if game_state.game_over:
            return None
        
        # Activate sacrifice mode if bot has more pieces
        black_count, white_count = self._count_pieces(game_state.board)
        self.sacrifice_mode = black_count > white_count + 2
        
        # Handle capture chain
        if game_state.must_capture and game_state.capturing_piece:
            return self._get_chain_capture(game_state)
        
        # Get all moves
        all_moves = game_state.board.get_all_valid_moves('black')
        if not all_moves:
            return None
        
        # Find capture moves
        capture_moves = []
        for piece, moves in all_moves.items():
            for move, captured in moves.items():
                if captured:
                    capture_moves.append(((piece.row, piece.col), move, 
                                         len(captured), piece))
        
        # Prefer captures in suicide mode
        if capture_moves:
            return self._select_bad_capture(capture_moves, game_state)
        
        # No captures, choose regular move
        return self._select_bad_move(all_moves, game_state)
    
    def _get_chain_capture(self, game_state):
        """Continue capture chain."""
        piece = game_state.capturing_piece
        if not piece:
            return None
        
        moves = game_state.board.get_valid_moves(piece)
        capture_options = [(move, len(captured)) for move, captured in moves.items() if captured]
        
        if not capture_options:
            return None
        
        if self.difficulty == "SUICIDE":
            # Choose capture with highest danger (worst for us)
            options_with_danger = []
            for move, num_captured in capture_options:
                danger = self._evaluate_position_danger(move[0], move[1], game_state)
                # Penalize for capturing pieces (bad in suicide)
                danger -= num_captured * 20
                options_with_danger.append((move, danger))
            
            options_with_danger.sort(key=lambda x: -x[1])  # Highest danger first
            return (piece.row, piece.col), options_with_danger[0][0]
        else:
            # Normal: capture fewest pieces
            capture_options.sort(key=lambda x: x[1])  # Fewest captured first
            return (piece.row, piece.col), capture_options[0][0]
    
    def _select_bad_capture(self, capture_moves, game_state):
        """Select worst capture move (for suicide strategy)."""
        scored_moves = []
        
        for src, dst, num_captured, piece in capture_moves:
            score = 0
            
            # Big penalty for capturing opponent pieces
            score -= num_captured * 15
            
            # Danger at destination (good for suicide)
            score += self._evaluate_position_danger(dst[0], dst[1], game_state) * 3
            
            # Avoid becoming king
            if not piece.king:
                if piece.color == 'black' and dst[0] == 7:  # Promotion row
                    score -= 100
                elif piece.color == 'white' and dst[0] == 0:
                    score -= 100
            
            # Isolated position (good)
            isolation = self._check_isolation(dst[0], dst[1], 'black', game_state.board)
            score += isolation * 2
            
            scored_moves.append((src, dst, score))
        
        # Choose move with highest score (worst for bot)
        scored_moves.sort(key=lambda x: -x[2])
        return scored_moves[0][0], scored_moves[0][1]
    
    def _select_bad_move(self, all_moves, game_state):
        """Select worst regular move."""
        scored_moves = []
        
        for piece, moves in all_moves.items():
            for move in moves.keys():
                score = 0
                
                # Danger at destination
                score += self._evaluate_position_danger(move[0], move[1], game_state) * 4
                
                # Move backwards (good for suicide)
                if not piece.king:
                    if piece.color == 'black' and move[0] < piece.row:
                        score += 20
                    elif piece.color == 'white' and move[0] > piece.row:
                        score += 20
                
                # Avoid promotion
                if not piece.king:
                    if piece.color == 'black' and move[0] == 7:
                        score -= 150
                    elif piece.color == 'white' and move[0] == 0:
                        score -= 150
                
                # King wants to die
                if piece.king:
                    score += 30
                
                # Avoid edges and corners (too safe)
                if (move[0] == 0 or move[0] == 7) and (move[1] == 0 or move[1] == 7):
                    score -= 30
                elif move[0] == 0 or move[0] == 7 or move[1] == 0 or move[1] == 7:
                    score -= 15
                
                scored_moves.append(((piece.row, piece.col), move, score))
        
        if not scored_moves:
            return self._get_random_move(all_moves)
        
        scored_moves.sort(key=lambda x: -x[2])
        return scored_moves[0][0], scored_moves[0][1]
    
    def _evaluate_position_danger(self, row, col, game_state):
        """Evaluate how dangerous a position is (higher = more likely to be captured)."""
        danger = 0
        board = game_state.board.board
        
        # Check if any enemy can capture from this position
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            enemy_r, enemy_c = row + dr, col + dc
            jump_r, jump_c = row - dr, col - dc
            
            if (0 <= enemy_r < 8 and 0 <= enemy_c < 8 and
                0 <= jump_r < 8 and 0 <= jump_c < 8):
                
                enemy = board[enemy_r][enemy_c]
                jump_cell = board[jump_r][jump_c]
                
                if enemy and enemy.color == 'white' and jump_cell is None:
                    danger += 30
                    if enemy.king:
                        danger += 20
        
        return danger
    
    def _check_isolation(self, row, col, color, board):
        """Check how isolated a piece is (isolated = good for suicide)."""
        allies = 0
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board.board[r][c]
                if piece and piece.color == color:
                    allies += 1
        
        if allies == 0:
            return 25  # Completely isolated
        elif allies == 1:
            return 8
        elif allies == 2:
            return 2
        else:
            return -20  # Too many allies
    
    def _count_pieces(self, board):
        """Count pieces for each side."""
        black = white = 0
        for row in board.board:
            for piece in row:
                if piece:
                    if piece.color == 'black':
                        black += 1
                    else:
                        white += 1
        return black, white
    
    def _get_random_move(self, all_moves):
        """Select random move as fallback."""
        pieces = list(all_moves.keys())
        if not pieces:
            return None
        
        piece = random.choice(pieces)
        moves = list(all_moves[piece].keys())
        
        if moves:
            return (piece.row, piece.col), random.choice(moves)
        
        return None
    