from piece import Piece
from constants import ROWS, COLS

class Board:
    def __init__(self):
        self.board = []
        self.white_left = 12
        self.black_left = 12
        self.white_kings = 0
        self.black_kings = 0
        self.create_board()
    
    def create_board(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
        for row in range(3):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece(row, col, 'black')
        
        for row in range(5, 8):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece(row, col, 'white')
    
    def get_piece(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None
    
    def move(self, piece, row, col, captured=None):
        self.board[piece.row][piece.col] = None
        
        if captured:
            self.remove(captured)
        
        self.board[row][col] = piece
        piece.move(row, col)
        
        if not piece.king:
            if piece.color == 'white' and row == 0:
                piece.make_king()
                self.white_kings += 1
            elif piece.color == 'black' and row == ROWS - 1:
                piece.make_king()
                self.black_kings += 1
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece.color == 'white':
                self.white_left -= 1
                if piece.king:
                    self.white_kings -= 1
            else:
                self.black_left -= 1
                if piece.king:
                    self.black_kings -= 1
    
    def get_valid_moves(self, piece):
        moves = {}
        
        directions = []
        
        if piece.king:
            if piece.color == 'white':
                directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            else:
                directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            if piece.color == 'white':
                directions = [(-1, -1), (-1, 1)]
            else:
                directions = [(1, -1), (1, 1)]
        
        for dr, dc in directions:
            moves.update(self._check_direction(piece, dr, dc))
        
        return moves
    
    def _check_direction(self, piece, dr, dc):
        moves = {}
        row = piece.row + dr
        col = piece.col + dc
        
        if not (0 <= row < ROWS and 0 <= col < COLS):
            return moves
        
        target = self.board[row][col]
        
        if target is None:
            moves[(row, col)] = []
        elif target.color != piece.color:
            jump_row = row + dr
            jump_col = col + dc
            
            if 0 <= jump_row < ROWS and 0 <= jump_col < COLS:
                if self.board[jump_row][jump_col] is None:
                    moves[(jump_row, jump_col)] = [target]
                    
                    if piece.king:
                        further_moves = self._check_king_captures(piece, jump_row, jump_col, dr, dc, [target])
                        moves.update(further_moves)
                    else:
                        further_moves = self._check_captures(piece, jump_row, jump_col, [target])
                        moves.update(further_moves)
        
        return moves
    
    def _check_captures(self, piece, start_row, start_col, captured):
        moves = {}
        
        directions = []
        if piece.color == 'white':
            directions = [(-1, -1), (-1, 1)]
        else:
            directions = [(1, -1), (1, 1)]
        
        for dr, dc in directions:
            row = start_row + dr
            col = start_col + dc
            
            if not (0 <= row < ROWS and 0 <= col < COLS):
                continue
            
            target = self.board[row][col]
            
            if target and target.color != piece.color:
                jump_row = row + dr
                jump_col = col + dc
                
                if 0 <= jump_row < ROWS and 0 <= jump_col < COLS:
                    if self.board[jump_row][jump_col] is None:
                        already_captured = any(c.row == target.row and c.col == target.col for c in captured)
                        if not already_captured:
                            moves[(jump_row, jump_col)] = captured + [target]
                            
                            further_moves = self._check_captures(piece, jump_row, jump_col, captured + [target])
                            moves.update(further_moves)
        
        return moves
    
    def _check_king_captures(self, piece, start_row, start_col, last_dr, last_dc, captured):
        moves = {}
        
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            row = start_row + dr
            col = start_col + dc
            
            if not (0 <= row < ROWS and 0 <= col < COLS):
                continue
            
            target = self.board[row][col]
            
            if target and target.color != piece.color:
                jump_row = row + dr
                jump_col = col + dc
                
                if 0 <= jump_row < ROWS and 0 <= jump_col < COLS:
                    if self.board[jump_row][jump_col] is None:
                        already_captured = any(c.row == target.row and c.col == target.col for c in captured)
                        if not already_captured:
                            moves[(jump_row, jump_col)] = captured + [target]
                            
                            further_moves = self._check_king_captures(piece, jump_row, jump_col, dr, dc, captured + [target])
                            moves.update(further_moves)
        
        return moves
    
    def get_all_pieces(self, color):
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def get_all_valid_moves(self, color):
        all_moves = {}
        pieces = self.get_all_pieces(color)
        
        has_captures = False
        
        for piece in pieces:
            moves = self.get_valid_moves(piece)
            piece_captures = {}
            
            for move, captured in moves.items():
                if captured:
                    has_captures = True
                    piece_captures[move] = captured
            
            if piece_captures:
                all_moves[piece] = piece_captures
        
        if has_captures:
            return all_moves
        
        all_moves = {}
        for piece in pieces:
            moves = self.get_valid_moves(piece)
            if moves:
                all_moves[piece] = moves
        
        return all_moves
    
    def winner(self):
        white_moves = self.get_all_valid_moves('white')
        black_moves = self.get_all_valid_moves('black')
        
        if not white_moves:
            return 'black'
        elif not black_moves:
            return 'white'
        
        return None