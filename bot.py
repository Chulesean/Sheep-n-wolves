import random

class PoddavkiBot:
    def __init__(self, difficulty="SUICIDE"):
        self.difficulty = difficulty
    
    def get_move(self, game_state):
        if game_state.game_over:
            return None
        
        if game_state.must_capture and game_state.capturing_piece:
            return self._get_chain_capture(game_state)
        
        all_moves = game_state.board.get_all_valid_moves('black')
        
        if not all_moves:
            return None
        
        capture_moves = []
        for piece, moves in all_moves.items():
            for move, captured in moves.items():
                if captured:
                    capture_moves.append(((piece.row, piece.col), move, len(captured), piece))
        
        if capture_moves:
            if self.difficulty == "SUICIDE":
                return self._select_suicide_capture(capture_moves, game_state)
            else:
                capture_moves.sort(key=lambda x: x[2], reverse=True)
                return capture_moves[0][0], capture_moves[0][1]
        
        if self.difficulty == "SUICIDE":
            return self._select_suicide_move(all_moves, game_state)
        else:
            return self._get_random_move(all_moves)
    
    def _get_chain_capture(self, game_state):
        piece = game_state.capturing_piece
        if not piece:
            return None
        
        moves = game_state.board.get_valid_moves(piece)
        
        capture_options = []
        for move, captured in moves.items():
            if captured:
                capture_options.append((move, len(captured)))
        
        if capture_options:
            if self.difficulty == "SUICIDE":
                capture_options.sort(key=lambda x: x[1])
            else:
                capture_options.sort(key=lambda x: x[1], reverse=True)
            return (piece.row, piece.col), capture_options[0][0]
        
        return None
    
    def _select_suicide_capture(self, capture_moves, game_state):
        best_danger = -10000
        best_move = None
        
        for src, dst, num_captured, piece in capture_moves:
            danger = self._evaluate_capture_danger(piece, dst, num_captured, game_state)
            
            if danger > best_danger:
                best_danger = danger
                best_move = (src, dst)
        
        if best_move:
            return best_move
        
        return capture_moves[0][0], capture_moves[0][1]
    
    def _evaluate_capture_danger(self, piece, move, num_captured, game_state):
        score = 0
        
        score -= num_captured * 8
        
        pos_danger = self._calculate_position_danger(move[0], move[1], game_state)
        score += pos_danger * 4
        
        if not piece.king:
            if piece.color == 'black' and move[0] == 7:
                score -= 30
            elif piece.color == 'white' and move[0] == 0:
                score -= 30
        
        if piece.king:
            score += 12
        
        isolation = self._check_isolation(move[0], move[1], 'black', game_state.board)
        score += isolation * 3
        
        if move[0] == 0 or move[0] == 7 or move[1] == 0 or move[1] == 7:
            score -= 8
        
        return score
    
    def _select_suicide_move(self, all_moves, game_state):
        best_danger = -10000
        best_move = None
        
        for piece, moves in all_moves.items():
            for move in moves.keys():
                danger = self._evaluate_move_danger(piece, move, game_state)
                
                if danger > best_danger:
                    best_danger = danger
                    best_move = ((piece.row, piece.col), move)
        
        if best_move:
            return best_move
        
        return self._get_random_move(all_moves)
    
    def _evaluate_move_danger(self, piece, move, game_state):
        score = 0
        
        pos_danger = self._calculate_position_danger(move[0], move[1], game_state)
        score += pos_danger * 6
        
        if piece.color == 'black':
            if move[0] <= piece.row:
                score += 5
            else:
                score -= 2
        else:
            if move[0] >= piece.row:
                score += 5
            else:
                score -= 2
        
        if not piece.king:
            if piece.color == 'black' and move[0] == 7:
                score -= 40
            elif piece.color == 'white' and move[0] == 0:
                score -= 40
        
        if piece.king:
            score += 18
        
        isolation = self._check_isolation(move[0], move[1], 'black', game_state.board)
        score += isolation * 4
        
        if move[0] == 0 or move[0] == 7 or move[1] == 0 or move[1] == 7:
            score -= 10
        
        center_rows = [3, 4]
        center_cols = [3, 4]
        if move[0] in center_rows and move[1] in center_cols:
            score += 8
        
        return score
    
    def _calculate_position_danger(self, row, col, game_state):
        danger = 0
        board = game_state.board.board
        
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece and piece.color == 'white':
                    check_r, check_c = row - dr, col - dc
                    if 0 <= check_r < 8 and 0 <= check_c < 8:
                        if board[check_r][check_c] is None:
                            danger += 15
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece and piece.color == 'white':
                    danger += 5
        
        if 2 <= row <= 5 and 2 <= col <= 5:
            danger += 6
        
        return danger
    
    def _check_isolation(self, row, col, color, board):
        isolation = 0
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        ally_count = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board.board[r][c]
                if piece and piece.color == color:
                    ally_count += 1
        
        if ally_count == 0:
            isolation += 10
        elif ally_count == 1:
            isolation += 4
        elif ally_count >= 3:
            isolation -= 5
        
        return isolation
    
    def _get_random_move(self, all_moves):
        pieces = list(all_moves.keys())
        if not pieces:
            return None
        
        piece = random.choice(pieces)
        moves = list(all_moves[piece].keys())
        
        if moves:
            return (piece.row, piece.col), random.choice(moves)
        
        return None