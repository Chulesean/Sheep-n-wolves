import pygame


class GameController:
    """
    Handles user input and mediates interactions between
    the player, game state, board, and assets.
    """

    def __init__(self, assets=None, board=None, game_state=None):
        """
        Initialize the game controller.

        :param assets: GameAssets instance for board layout and sizes
        :param board: Board instance containing game logic
        :param game_state: GameState instance managing turns and selections
        """
        self.assets = assets
        self.board = board
        self.state = game_state
        self.vs_bot = False

    def set_vs_bot(self, enabled):
        """
        Enable or disable playing against a bot.

        :param enabled: True to enable bot mode, False otherwise
        """
        self.vs_bot = enabled

    def get_clicked_position(self, mouse_pos):
        """
        Convert a mouse position to a board row and column.

        :param mouse_pos: (x, y) mouse position in screen coordinates
        :return: (row, col) if inside the board, otherwise (None, None)
        """
        if not self.assets:
            return None, None

        board_left, board_top = self.assets.board_topleft
        square_size = self.assets.square_size

        x, y = mouse_pos

        if (
            board_left <= x < board_left + 8 * square_size and
            board_top <= y < board_top + 8 * square_size
        ):
            col = (x - board_left) // square_size
            row = (y - board_top) // square_size
            return row, col

        return None, None

    def handle_click(self, mouse_pos):
        """
        Handle a mouse click event.

        Selects a piece or performs a move if the click is valid.
        Player input is ignored when the game is over or when
        it is the bot's turn in bot mode.

        :param mouse_pos: (x, y) mouse position
        """
        if not self.state or self.state.game_over:
            return

        # If playing against a bot and it is the bot's turn,
        # ignore player input
        if self.vs_bot and self.state.turn == 'black':
            return

        row, col = self.get_clicked_position(mouse_pos)
        if row is not None and col is not None:
            self.state.select(row, col)

    def handle_keydown(self, event):
        """
        Handle keyboard input.

        :param event: Pygame KEYDOWN event
        :return: Action string ('exit', 'reset') or None
        """
        if event.key == pygame.K_ESCAPE:
            return 'exit'
        elif event.key == pygame.K_r:
            return 'reset'
        return None
