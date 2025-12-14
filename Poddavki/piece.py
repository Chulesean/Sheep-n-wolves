class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.selected = False
    
    def make_king(self):
        self.king = True
    
    def move(self, row, col):
        self.row = row
        self.col = col
    
    def __repr__(self):
        return f"{self.color}{'K' if self.king else 'M'}({self.row},{self.col})"