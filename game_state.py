import pygame

class GameState:
    def __init__(self, board):
        self.board = board
        self.turn = 'white'
        self.selected = None
        self.valid_moves = {}
        self.capturing_piece = None
        self.capture_chain = []
        self.must_capture = False
        self.game_over = False
        self.winner = None
        self.win_reason = ""
        self.FONT = pygame.font.SysFont(None, 40)
 
        self._check_mandatory_captures()
    
    def _check_mandatory_captures(self):
        all_moves = self.board.get_all_valid_moves(self.turn)
        has_captures = False
        
        for piece, moves in all_moves.items():
            for captured in moves.values():
                if captured:
                    has_captures = True
                    break
            if has_captures:
                break
        
        self.must_capture = has_captures

        if self.must_capture and self.selected:
            self._update_selected_moves()
    
    def _update_selected_moves(self):
        if self.selected:
            moves = self.board.get_valid_moves(self.selected)
            if self.must_capture:
                self.valid_moves = {move: captured for move, captured in moves.items() if captured}
            else:
                self.valid_moves = moves
    
    def select(self, row, col):
        if self.game_over:
            return False
        
        piece = self.board.get_piece(row, col)
        
        if self.must_capture and self.capturing_piece:
            if piece == self.capturing_piece:
                return True
            elif (row, col) in self.valid_moves:
                self._move(row, col)
                return True
            return False
        
        if piece and piece.color == self.turn:
            if self.must_capture:
                moves = self.board.get_valid_moves(piece)
                has_capture = any(captured for captured in moves.values())
                
                if not has_capture:
                    return False
            
            if self.selected:
                self.selected.selected = False
            
            self.selected = piece
            self.selected.selected = True
            self.valid_moves = self.board.get_valid_moves(piece)
            
            if self.must_capture:
                self.valid_moves = {move: captured for move, captured in self.valid_moves.items() if captured}
                if not self.valid_moves:
                    self.selected.selected = False
                    self.selected = None
                    return False
            
            return True
        
        elif self.selected and (row, col) in self.valid_moves:
            self._move(row, col)
            return True
        
        else:
            if self.selected:
                self.selected.selected = False
                self.selected = None
                self.valid_moves = {}
            return False
    
    def _move(self, row, col):
        piece = self.selected
        captured = self.valid_moves[(row, col)]
        
        self.board.move(piece, row, col, captured)
        
        if captured:
            self.capture_chain.extend(captured)
            
            self.selected = piece
            moves = self.board.get_valid_moves(piece)
            
            new_valid_moves = {}
            for move, new_captured in moves.items():
                if new_captured:
                    already_captured = any(
                        c.row == new_captured[0].row and c.col == new_captured[0].col
                        for c in self.capture_chain
                    )
                    if not already_captured:
                        new_valid_moves[move] = new_captured
            
            self.valid_moves = new_valid_moves
            
            if self.valid_moves:
                self.must_capture = True
                self.capturing_piece = piece
                return
        
        self._end_turn()
    
    def _end_turn(self):
        if self.selected:
            self.selected.selected = False
        self.selected = None
        self.valid_moves = {}
        self.capturing_piece = None
        self.capture_chain = []
        
        self._check_winner()
        
        if self.game_over:
            return
        
        self.turn = 'black' if self.turn == 'white' else 'white'
        
        self._check_mandatory_captures()
    
    def _check_winner(self):
        white_moves = self.board.get_all_valid_moves('white')
        black_moves = self.board.get_all_valid_moves('black')
                
        if not white_moves:
            self.game_over = True
            self.winner = 'white'   
            self.win_reason = "White's out of moves!"
            
        elif not black_moves:
            self.game_over = True
            self.winner = 'black'  
            self.win_reason = "Black's out of moves!"