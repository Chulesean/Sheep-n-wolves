import random
import pygame
from bot import NineMensMorrisBot
import time

class GameController:
    def __init__(self, board_geometry, game_state):
        self.board = board_geometry
        self.state = game_state
        self.bot = None
        self.vs_bot = False
        self.last_bot_move_time = 0
        self.bot_delay = 1.0
        self.bot_thinking = False

    def set_vs_bot(self, enabled):
        self.vs_bot = enabled
        if enabled:
            self.bot = NineMensMorrisBot("EASY")

    def nearest_point(self, mouse_pos):
        for i, point in enumerate(self.board.points):
            if self.distance(mouse_pos, point) < 25:
                return i
        return None

    def distance(self, pos1, pos2):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def handle_click(self, idx):
        if self.state.winner or self.bot_thinking:
            return

        if self.vs_bot and self.state.turn == "B":
            return

        mover = self.state.turn
        opponent = "B" if mover == "W" else "W"

        if self.state.capturing:
            self.handle_capture(idx, mover, opponent)
        elif self.state.phase == "placement":
            self.handle_placement(idx, mover)
        else:
            self.handle_movement(idx, mover)

    def handle_capture(self, idx, mover, opponent):
        if self.state.occupied[idx] == opponent:
            opponent_pieces = [p for p in range(24) if self.state.occupied[p] == opponent]
            non_mill_pieces = [p for p in opponent_pieces if not self.state.is_mill(p, opponent)]

            if not non_mill_pieces or not self.state.is_mill(idx, opponent):
                self.state.occupied[idx] = None
                self.state.capturing = False
                self.state.selected_piece = None

            # QUAN TRỌNG: Chỉ kiểm tra thắng trong phase moving
                if self.state.phase == "moving":
                    self.state.check_win_conditions(mover)
                    if not self.state.winner:
                        self.state.switch_turn()
                else:
                # Trong phase placement, luôn chuyển lượt
                    self.state.switch_turn()

    def handle_placement(self, idx, mover):
        if self.state.placed[mover] >= 9:
            return
            
        if self.state.occupied[idx] is None:
            self.state.occupied[idx] = mover
            self.state.placed[mover] += 1
            
            if self.state.is_mill(idx, mover):
                self.state.capturing = True
            else:
                self.state.switch_turn()

    def handle_movement(self, idx, mover):
        if self.state.selected_piece is None:
            if self.state.occupied[idx] == mover:
                self.state.selected_piece = idx
        else:
            if self.state.valid_move(self.state.selected_piece, idx, mover):
                self.state.occupied[idx] = mover
                self.state.occupied[self.state.selected_piece] = None
                
                if self.state.is_mill(idx, mover):
                    self.state.capturing = True
                else:
                    self.state.switch_turn()
                self.state.selected_piece = None
            elif self.state.occupied[idx] == mover:
                self.state.selected_piece = idx

    def update(self):
        if self.state.winner:
            return

        current_time = time.time()
        bot_timeout = 3.0
        if (self.vs_bot and self.state.turn == "B" and self.bot and 
            current_time - self.last_bot_move_time >= self.bot_delay and
            not self.bot_thinking):
            
            self.bot_thinking = True
            
            try:
                # QUAN TRỌNG: Xử lý capture trước
                if self.state.capturing:
                    
                    capture_move = self.get_bot_capture_move()
                    if capture_move is not None:
                        self.execute_bot_capture(capture_move)
                    else:
                        # Nếu không tìm được quân để bắt, thoát khỏi trạng thái capturing
                        self.state.capturing = False
                        self.state.switch_turn()
                else:
                    # Bot di chuyển bình thường
                    
                    move = self.bot.get_move(self.state)
                    if move:
                        self.execute_bot_move(move)
                    else:
                        # Nếu không có nước đi hợp lệ, chuyển lượt
                        self.state.switch_turn()
                        
            except Exception as e:
                print(f"Bot error: {e}")
                # Nếu có lỗi, thoát khỏi trạng thái capturing và chuyển lượt
                self.state.capturing = False
                self.state.switch_turn()
            
            finally:
                self.last_bot_move_time = current_time
                self.bot_thinking = False

    def get_bot_capture_move(self):
        "bot choosing an opponent's piece"
        try:
            opponent_pieces = [p for p in range(24) if self.state.occupied[p] == "W"]
            if not opponent_pieces:
                return None
            
            # Tìm quân không trong mill trước
            non_mill_pieces = [p for p in opponent_pieces if not self.state.is_mill(p, "W")]
            if non_mill_pieces:
                return random.choice(non_mill_pieces)
            else:
                # Nếu tất cả đều trong mill, bắt quân bất kỳ
                return random.choice(opponent_pieces)
                
        except Exception as e:
            print(f"Error in get_bot_capture_move: {e}")
            return None

    def execute_bot_capture(self, target_pos):
        "capturing"
        try:
            if 0 <= target_pos < 24 and self.state.occupied[target_pos] == "W":
                self.state.occupied[target_pos] = None
                self.state.capturing = False
            
                if self.state.phase == "moving":
                    self.state.check_win_conditions("B")
                    if not self.state.winner:
                        self.state.switch_turn()
                else:
                    self.state.switch_turn()
                    
        except Exception as e:
            print(f"Error in execute_bot_capture: {e}")
        # Khôi phục trạng thái an toàn
            self.state.capturing = False
            self.state.switch_turn()

    def execute_bot_move(self, move):
        """Bot moves"""
        try:
            if self.state.phase == "placement":
                if self.state.placed["B"] >= 9:
                    return
                    
                # Đảm bảo move là số nguyên
                if isinstance(move, int) and 0 <= move < 24 and self.state.occupied[move] is None:
                    self.state.occupied[move] = "B"
                    self.state.placed["B"] += 1
                    
                    if self.state.is_mill(move, "B"):
                        self.state.capturing = True
                        
                    else:
                        self.state.switch_turn()
                        
            else:
                # Di chuyển phase
                if isinstance(move, tuple) and len(move) == 2:
                    src, dst = move
                    if (0 <= src < 24 and 0 <= dst < 24 and 
                        self.state.occupied[src] == "B" and 
                        self.state.occupied[dst] is None and
                        self.state.valid_move(src, dst, "B")):
                        
                        self.state.occupied[dst] = "B"
                        self.state.occupied[src] = None
                        
                        if self.state.is_mill(dst, "B"):
                            self.state.capturing = True
                            
                        else:
                            self.state.switch_turn()
                            
        except Exception as e:
            print(f"Error in execute_bot_move: {e}")
            # Khôi phục trạng thái an toàn
            self.state.capturing = False
            self.state.switch_turn()
