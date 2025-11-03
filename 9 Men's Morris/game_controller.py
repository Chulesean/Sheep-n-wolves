import math

class GameController:
    def __init__(self, board_geometry, game_state):
        self.board = board_geometry
        self.state = game_state
    
    def nearest_point(self, mouse_pos):
        for i, point in enumerate(self.board.points):
            if math.dist(mouse_pos, point) < 25:
                return i
        return None
    
    def handle_click(self, idx):
        if self.state.winner:
            return
        
        mover, opponent = self.state.turn, "B" if self.state.turn == "W" else "W"
        
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
                
                if self.state.phase != "placement":
                    self.state.check_win_conditions(mover)
                    if not self.state.winner:
                        self.state.switch_turn()
                else:
                    self.state.switch_turn()
    
    def handle_placement(self, idx, mover):
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