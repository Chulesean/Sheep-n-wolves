"""
Asset management for Nine Men's Morris game.

Loads and scales all graphical assets including background, board, frame, and game pieces.
Calculates positions and sizes for proper rendering on screen.
"""

import pygame
from constants import COLORS, BOARD_SCALE, FRAME_MARGIN_SCALE, PIECE_SCALE

class GameAssets:
    """
    Asset management for Nine Men's Morris game.
    
    IMPORTANT: This class should be instantiated ONCE and reused throughout
    the game session. Assets are loaded and scaled during initialization.
    """
    
    def __init__(self, screen_w, screen_h, cx, cy):
        """
        Initialize and load all game assets.
        
        Note: This constructor loads images from disk and performs scaling.
        It should be called only once per game session.
        """
        self.board_size = int(min(screen_w, screen_h) * BOARD_SCALE)
        self.board_half = self.board_size // 2
        self.board_topleft = (cx - self.board_half, cy - self.board_half)
        
        self.background = self.load_asset("assets/background.png", screen_w, screen_h)
        
        # Frame extends 8% beyond board edges for visual padding
        frame_margin = int(self.board_size * FRAME_MARGIN_SCALE)
        frame_size = self.board_size + frame_margin
        self.frame = self.load_asset("assets/frame.png", frame_size, frame_size)
        self.frame_topleft = (cx - self.frame.get_width() // 2, cy - self.frame.get_height() // 2)
        
        self.board_img = self.load_asset("assets/board.png", self.board_size, self.board_size)

        # Piece size is 6% of board size - balanced visibility and spacing
        piece_size = int(self.board_size * PIECE_SCALE)
        self.white_piece_img = self.load_piece_image("assets/white_piece.png", piece_size, COLORS['WHITE'])
        self.black_piece_img = self.load_piece_image("assets/black_piece.png", piece_size, COLORS['BLACK'])
    
    def load_asset(self, name, w, h):
        """
        Load and scale an image asset with error handling.
        
        Args:
            name (str): Path to image file
            w (int): Desired width
            h (int): Desired height
            
        Returns:
            pygame.Surface: Loaded and scaled image, or fallback surface on error
        """
        try:
            # Determine if asset needs alpha channel
            if "background" in name:
                img = pygame.image.load(name).convert()  # Opaque background
            else:
                img = pygame.image.load(name).convert_alpha()  # Transparent assets
                
            return pygame.transform.smoothscale(img, (int(w), int(h)))
        except pygame.error as e:
            print(f"[ERROR] Failed to load image '{name}': {e}")
            # Create a fallback colored surface
            fallback = pygame.Surface((int(w), int(h)), pygame.SRCALPHA)
            if "background" in name:
                fallback.fill((50, 50, 80, 255))  # Dark blue for background
            elif "frame" in name:
                fallback.fill((100, 80, 60, 200))  # Brownish for frame
            elif "board" in name:
                fallback.fill((220, 200, 180, 255))  # Light brown for board
            else:
                fallback.fill((255, 0, 0, 100))  # Red for unknown
            return fallback
           
    def load_piece_image(self, filename, size, fallback_color):
        """
        Load and scale a game piece image with error handling.
        
        Args:
            filename (str): Path to piece image file
            size (int): Desired size (width and height)
            fallback_color (tuple): RGB color for fallback piece
            
        Returns:
            pygame.Surface: Loaded piece image, or generated fallback surface
        """
        try:
            img = pygame.image.load(filename).convert_alpha()
            return pygame.transform.smoothscale(img, (size, size))
        except pygame.error as e:
            print(f"[WARN] Failed to load piece image '{filename}': {e}. Using fallback.")
            # Create a circle as fallback
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Draw circle with color
            pygame.draw.circle(surface, fallback_color, (size // 2, size // 2), size // 2)
            
            # Add outline for white pieces
            if fallback_color == COLORS['WHITE']:
                pygame.draw.circle(surface, COLORS['BLACK'], (size // 2, size // 2), size // 2, 2)
            
            return surface
        
