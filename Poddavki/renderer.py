import pygame
from constants import COLORS


class GameRenderer:
    """
    Responsible for drawing all visual elements of the game,
    including the board, pieces, highlights, UI, and end-game screen.
    """

    def __init__(self, assets, board, game_state, screen, screen_w, screen_h):
        """
        Initialize the renderer.

        :param assets: GameAssets instance containing images and sizes
        :param board: Board instance with current game data
        :param game_state: GameState instance tracking turns and rules
        :param screen: Pygame display surface
        :param screen_w: Screen width
        :param screen_h: Screen height
        """
        self.assets = assets
        self.board = board
        self.state = game_state
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h

    def draw_background(self):
        """
        Draw the background image.
        """
        self.screen.blit(self.assets.background, (0, 0))

    def draw_frame(self):
        """
        Draw the decorative frame around the board.
        """
        self.screen.blit(self.assets.frame, self.assets.frame_topleft)

    def draw_board(self):
        """
        Draw the board grid and mandatory capture highlights.
        """
        self.screen.blit(self.assets.board_img, self.assets.board_topleft)
        self._draw_must_capture_highlight()

    def _draw_must_capture_highlight(self):
        """
        Highlight pieces that are required to capture.
        """
        if not self.state.must_capture:
            return

        square_size = self.assets.square_size
        board_left, board_top = self.assets.board_topleft

        pieces = self.board.get_all_pieces(self.state.turn)

        for piece in pieces:
            moves = self.board.get_valid_moves(piece)
            if any(captured for captured in moves.values()):
                x = board_left + piece.col * square_size
                y = board_top + piece.row * square_size

                highlight = pygame.Surface(
                    (square_size, square_size), pygame.SRCALPHA
                )
                highlight.fill((0, 255, 0, 60))
                self.screen.blit(highlight, (x, y))

    def draw_pieces(self):
        """
        Draw all pieces on the board, including selection outlines.
        """
        square_size = self.assets.square_size
        board_left, board_top = self.assets.board_topleft

        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece:
                    x = board_left + col * square_size + square_size // 2
                    y = board_top + row * square_size + square_size // 2

                    if piece.color == 'white':
                        img = (
                            self.assets.white_king_img
                            if piece.king
                            else self.assets.white_piece_img
                        )
                    else:
                        img = (
                            self.assets.black_king_img
                            if piece.king
                            else self.assets.black_piece_img
                        )

                    img_rect = img.get_rect(center=(x, y))
                    self.screen.blit(img, img_rect)

                    # Draw selection outline
                    if piece.selected:
                        pygame.draw.circle(
                            self.screen,
                            COLORS['GREEN'],
                            (x, y),
                            square_size // 2 - 5,
                            3
                        )

    def draw_valid_moves(self):
        """
        Highlight all valid move destinations for the selected piece.
        """
        if not self.state.selected:
            return

        square_size = self.assets.square_size
        board_left, board_top = self.assets.board_topleft

        for (row, col), captured in self.state.valid_moves.items():
            x = board_left + col * square_size
            y = board_top + row * square_size

            highlight = pygame.Surface(
                (square_size - 10, square_size - 10),
                pygame.SRCALPHA
            )

            if captured:
                highlight.fill(COLORS['CAPTURE_HIGHLIGHT'])

                # Show number of captures in chain
                font = pygame.font.SysFont(None, 24)
                text = font.render(str(len(captured)), True, COLORS['WHITE'])
                text_rect = text.get_rect(
                    center=(square_size // 2 - 5, square_size // 2 - 5)
                )
                highlight.blit(text, text_rect)
            else:
                highlight.fill(COLORS['MOVE_HIGHLIGHT'])

            self.screen.blit(
                highlight,
                (x + 5, y + 5)
            )

    def draw_ui(self):
        """
        Draw the top UI bar with turn info, piece counts, and warnings.
        """
        info_height = 60
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),
            (0, 0, self.screen_w, info_height)
        )

        turn_color = (
            COLORS['WHITE']
            if self.state.turn == 'white'
            else COLORS['BLACK']
        )
        turn_text = f"Turn: {self.state.turn.upper()}"
        turn_surface = self.state.FONT.render(turn_text, True, turn_color)
        self.screen.blit(turn_surface, (20, 10))

        white_text = f"WHITE: {self.board.white_left}"
        black_text = f"BLACK: {self.board.black_left}"

        white_surf = self.state.FONT.render(white_text, True, COLORS['WHITE'])
        black_surf = self.state.FONT.render(black_text, True, COLORS['BLACK'])

        self.screen.blit(white_surf, (self.screen_w - 150, 10))
        self.screen.blit(black_surf, (self.screen_w - 150, 40))

        if self.state.must_capture:
            warning_font = pygame.font.SysFont(None, 32)
            warning = warning_font.render(
                "CAPTURE MANDATORY", True, COLORS['RED']
            )
            self.screen.blit(warning, (self.screen_w // 2 - 100, 10))

        if self.state.game_over:
            self.draw_game_over()

    def draw_game_over(self):
        """
        Draw the game-over overlay and winner information.
        """
        overlay = pygame.Surface(
            (self.screen_w, self.screen_h), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.SysFont(None, 72)
        font_medium = pygame.font.SysFont(None, 36)

        winner_text = (
            "WHITE WINS!" if self.state.winner == 'white' else "BLACK WINS!"
        )
        winner_color = (
            COLORS['WHITE']
            if self.state.winner == 'white'
            else COLORS['BLACK']
        )

        text = font_large.render(winner_text, True, winner_color)
        text_rect = text.get_rect(
            center=(self.screen_w // 2, self.screen_h // 2 - 50)
        )
        self.screen.blit(text, text_rect)

        reason_text = (
            "White's out of moves!"
            if self.state.winner == 'white'
            else "Black's out of moves!"
        )
        reason = font_medium.render(reason_text, True, COLORS['WHITE'])
        reason_rect = reason.get_rect(
            center=(self.screen_w // 2, self.screen_h // 2 + 20)
        )
        self.screen.blit(reason, reason_rect)

        restart_text = font_medium.render(
            "Press ESC to exit", True, COLORS['WHITE']
        )
        restart_rect = restart_text.get_rect(
            center=(self.screen_w // 2, self.screen_h // 2 + 80)
        )
        self.screen.blit(restart_text, restart_rect)
