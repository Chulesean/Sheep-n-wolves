import pygame


class GameState:
    """
    Manages the current state of the game, including turn handling,
    piece selection, move validation, captures, and win conditions.
    """

    def __init__(self, board):
        """
        Initialize the game state.

        :param board: Board instance containing the game logic
        """
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
        """
        Check whether the current player has any mandatory capture moves.
        """
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
        """
        Update valid moves for the currently selected piece,
        enforcing capture-only moves if required.
        """
        if self.selected:
            moves = self.board.get_valid_moves(self.selected)
            if self.must_capture:
                self.valid_moves = {
                    move: captured
                    for move, captured in moves.items()
                    if captured
                }
            else:
                self.valid_moves = moves

    def select(self, row, col):
        """
        Handle selection or movement based on a board click.

        :param row: Clicked row
        :param col: Clicked column
        :return: True if action was successful, False otherwise
        """
        if self.game_over:
            return False

        piece = self.board.get_piece(row, col)

        # Continue a forced capture chain
        if self.must_capture and self.capturing_piece:
            if piece == self.capturing_piece:
                return True
            elif (row, col) in self.valid_moves:
                self._move(row, col)
                return True
            return False

        # Select a piece
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
                self.valid_moves = {
                    move: captured
                    for move, captured in self.valid_moves.items()
                    if captured
                }
                if not self.valid_moves:
                    self.selected.selected = False
                    self.selected = None
                    return False

            return True

        # Perform a move
        elif self.selected and (row, col) in self.valid_moves:
            self._move(row, col)
            return True

        # Deselect
        else:
            if self.selected:
                self.selected.selected = False
                self.selected = None
                self.valid_moves = {}
            return False

    def _move(self, row, col):
        """
        Execute a move and handle capture chains.
        """
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
        """
        End the current turn and switch to the other player.
        """
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
        """
        Check if the game has ended and determine the winner.
        """
        white_moves = self.board.get_all_valid_moves('white')
        black_moves = self.board.get_all_valid_moves('black')

        if not white_moves:
            self.game_over = True
            self.winner = 'white'
            self.win_reason = "White is out of moves!"

        elif not black_moves:
            self.game_over = True
            self.winner = 'black'
            self.win_reason = "Black is out of moves!"

    def reset_with_bot_first(self, board):
        """
        Reset the game state with the bot going first (black).

        :param board: New Board instance
        """
        self.board = board
        self.turn = 'black'  # Bot always goes first
        self.selected = None
        self.valid_moves = {}
        self.capturing_piece = None
        self.capture_chain = []
        self.must_capture = False
        self.game_over = False
        self.winner = None
        self.win_reason = ""

        self._check_mandatory_captures()
