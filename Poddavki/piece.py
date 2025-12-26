class Piece:
    """
    Represents a single game piece on the board.
    A piece can be either a normal piece or a king.
    """

    def __init__(self, row, col, color):
        """
        Initialize a game piece.

        :param row: Initial row position
        :param col: Initial column position
        :param color: Piece color ('white' or 'black')
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.selected = False

    def make_king(self):
        """
        Promote this piece to a king.
        """
        self.king = True

    def move(self, row, col):
        """
        Update the piece's position.

        :param row: New row position
        :param col: New column position
        """
        self.row = row
        self.col = col

    def __repr__(self):
        """
        Return a string representation of the piece,
        useful for debugging.
        """
        return f"{self.color}{'K' if self.king else 'M'}({self.row},{self.col})"
