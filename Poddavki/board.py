from piece import Piece
from constants import ROWS, COLS


class Board:
    """
    Represents the game board and handles all board-related logic,
    including piece placement, movement, captures, and win conditions.
    """

    def __init__(self):
        """
        Initialize the board state and piece counters.
        """
        self.board = []
        self.white_left = 12
        self.black_left = 12
        self.white_kings = 0
        self.black_kings = 0
        self.create_board()

    def create_board(self):
        """
        Create the initial board layout with pieces placed
        in standard starting positions.
        """
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]

        # Place black pieces on the top 3 rows
        for row in range(3):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece(row, col, 'black')

        # Place white pieces on the bottom 3 rows
        for row in range(5, 8):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece(row, col, 'white')

    def get_piece(self, row, col):
        """
        Get the piece at a specific board position.

        :param row: Row index
        :param col: Column index
        :return: Piece object or None if empty or out of bounds
        """
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None

    def move(self, piece, row, col, captured=None):
        """
        Move a piece to a new position and handle captures and promotion.

        :param piece: The piece to move
        :param row: Target row
        :param col: Target column
        :param captured: List of captured pieces (if any)
        """
        self.board[piece.row][piece.col] = None

        if captured:
            self.remove(captured)

        self.board[row][col] = piece
        piece.move(row, col)

        # Promote to king if reaching the opposite end
        if not piece.king:
            if piece.color == 'white' and row == 0:
                piece.make_king()
                self.white_kings += 1
            elif piece.color == 'black' and row == ROWS - 1:
                piece.make_king()
                self.black_kings += 1

    def remove(self, pieces):
        """
        Remove captured pieces from the board and update counters.

        :param pieces: List of pieces to remove
        """
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
        """
        Get all valid moves for a specific piece.

        :param piece: Piece to evaluate
        :return: Dictionary mapping (row, col) -> list of captured pieces
        """
        moves = {}
        directions = []

        # Determine movement directions
        if piece.king:
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
        """
        Check possible moves and captures in a specific direction.

        :param piece: Piece being evaluated
        :param dr: Row direction
        :param dc: Column direction
        :return: Dictionary of valid moves in that direction
        """
        moves = {}
        row = piece.row + dr
        col = piece.col + dc

        if not (0 <= row < ROWS and 0 <= col < COLS):
            return moves

        target = self.board[row][col]

        # Normal move
        if target is None:
            moves[(row, col)] = []

        # Capture move
        elif target.color != piece.color:
            jump_row = row + dr
            jump_col = col + dc

            if 0 <= jump_row < ROWS and 0 <= jump_col < COLS:
                if self.board[jump_row][jump_col] is None:
                    moves[(jump_row, jump_col)] = [target]

                    # Continue checking for multi-captures
                    if piece.king:
                        further_moves = self._check_king_captures(
                            piece, jump_row, jump_col, dr, dc, [target]
                        )
                    else:
                        further_moves = self._check_captures(
                            piece, jump_row, jump_col, [target]
                        )
                    moves.update(further_moves)

        return moves

    def _check_captures(self, piece, start_row, start_col, captured):
        """
        Recursively check for additional captures for a normal piece.

        :param piece: Piece being evaluated
        :param start_row: Current row
        :param start_col: Current column
        :param captured: List of already captured pieces
        :return: Dictionary of additional capture moves
        """
        moves = {}

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
                        already_captured = any(
                            c.row == target.row and c.col == target.col
                            for c in captured
                        )
                        if not already_captured:
                            moves[(jump_row, jump_col)] = captured + [target]
                            further_moves = self._check_captures(
                                piece,
                                jump_row,
                                jump_col,
                                captured + [target]
                            )
                            moves.update(further_moves)

        return moves

    def _check_king_captures(self, piece, start_row, start_col, last_dr, last_dc, captured):
        """
        Recursively check for additional captures for a king piece.

        :param piece: King piece being evaluated
        :param start_row: Current row
        :param start_col: Current column
        :param last_dr: Last row direction used
        :param last_dc: Last column direction used
        :param captured: List of already captured pieces
        :return: Dictionary of additional capture moves
        """
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
                        already_captured = any(
                            c.row == target.row and c.col == target.col
                            for c in captured
                        )
                        if not already_captured:
                            moves[(jump_row, jump_col)] = captured + [target]
                            further_moves = self._check_king_captures(
                                piece,
                                jump_row,
                                jump_col,
                                dr,
                                dc,
                                captured + [target]
                            )
                            moves.update(further_moves)

        return moves

    def get_all_pieces(self, color):
        """
        Get all pieces of a specific color.

        :param color: 'white' or 'black'
        :return: List of Piece objects
        """
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_all_valid_moves(self, color):
        """
        Get all valid moves for a given color, enforcing mandatory captures.

        :param color: 'white' or 'black'
        :return: Dictionary mapping Piece -> valid moves
        """
        all_moves = {}
        pieces = self.get_all_pieces(color)
        has_captures = False

        # First pass: check for captures
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

        # Second pass: allow normal moves if no captures exist
        all_moves = {}
        for piece in pieces:
            moves = self.get_valid_moves(piece)
            if moves:
                all_moves[piece] = moves

        return all_moves

    def winner(self):
        """
        Determine if there is a winner.

        :return: 'white', 'black', or None if the game is not over
        """
        white_moves = self.get_all_valid_moves('white')
        black_moves = self.get_all_valid_moves('black')

        if not white_moves:
            return 'black'
        elif not black_moves:
            return 'white'

        return None
