# test_king.py
from board import Board
from piece import Piece

def test_king_movement():
    print("=== TEST DI CHUYỂN VUA ===")
    
    board = Board()
    
    # Xóa tất cả quân để test
    for r in range(8):
        for c in range(8):
            board.board[r][c] = None
    
    # Tạo Vua trắng ở giữa (3,3)
    king = Piece(3, 3, 'white')
    king.make_king()
    board.board[3][3] = king
    
    print(f"Vua ở vị trí ({king.row},{king.col})")
    
    # Test di chuyển tự do
    moves = board.get_valid_moves(king)
    print(f"Số nước đi có thể: {len(moves)}")
    
    # Hiển thị bàn cờ
    print("\nBàn cờ (K = Vua, . = ô trống, X = có thể đi đến):")
    for r in range(8):
        row_str = ""
        for c in range(8):
            if r == 3 and c == 3:
                row_str += "K "
            elif (r, c) in moves:
                row_str += "X "
            elif board.board[r][c]:
                row_str += "P "
            else:
                row_str += ". "
        print(f"{r}: {row_str}")
    
    # Test ăn quân từ xa
    print("\n=== TEST ĂN QUÂN TỪ XA ===")
    
    # Đặt quân đen ở (1,1) - trên đường chéo của Vua
    enemy = Piece(1, 1, 'black')
    board.board[1][1] = enemy
    
    # Đặt quân đen ở (5,5) - đường chéo khác
    enemy2 = Piece(5, 5, 'black')
    board.board[5][5] = enemy2
    
    moves = board.get_valid_moves(king)
    capture_moves = [(pos, captured) for pos, captured in moves.items() if captured]
    
    print(f"Số nước ăn quân: {len(capture_moves)}")
    for (r, c), captured in capture_moves:
        print(f"  Ăn quân ở ({captured[0].row},{captured[0].col}) -> Đi đến ({r},{c})")
    
    # Hiển thị lại bàn cờ
    print("\nBàn cờ với quân đen:")
    for r in range(8):
        row_str = ""
        for c in range(8):
            if r == 3 and c == 3:
                row_str += "K "
            elif board.board[r][c]:
                if board.board[r][c].color == 'black':
                    row_str += "B "
                else:
                    row_str += "W "
            elif (r, c) in moves and moves[(r, c)]:
                row_str += "! "  # Nước ăn quân
            elif (r, c) in moves:
                row_str += "x "  # Nước di chuyển thường
            else:
                row_str += ". "
        print(f"{r}: {row_str}")

if __name__ == "__main__":
    test_king_movement()