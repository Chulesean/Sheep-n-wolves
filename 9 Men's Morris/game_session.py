"""
Game session manager for Nine Men's Morris.

Manages a single game session with proper initialization and cleanup.
Reuses assets to avoid reloading from disk multiple times.
"""

import pygame
from game_assets import GameAssets
from board_geometry import BoardGeometry
from game_state import GameState
from game_renderer import GameRenderer
from game_controller import GameController
from constants import RETURN_TO_MENU, QUIT_GAME, ScreenConfig

class GameSession:
    """Manages a single game session."""
    
    # Class-level cache for assets to avoid reloading
    _cached_assets = None
    _last_config = None
    
    def __init__(self, config: ScreenConfig, vs_bot: bool = False):
        """
        Initialize a game session.
        
        Args:
            config: Screen configuration
            vs_bot: Whether playing against bot
        """
        self.config = config
        self.vs_bot = vs_bot
        
        # Reuse assets if same screen configuration
        if (GameSession._cached_assets is None or 
            GameSession._last_config != (config.width, config.height, config.center_x, config.center_y)):
            
            GameSession._cached_assets = GameAssets(
                config.width, config.height, config.center_x, config.center_y
            )
            GameSession._last_config = (config.width, config.height, config.center_x, config.center_y)
        
        self.assets = GameSession._cached_assets
        
        # Create game components
        self.board_geo = BoardGeometry(self.assets.board_half, config.center_x, config.center_y)
        self.game_state = GameState(self.board_geo)
        self.renderer = GameRenderer(
            self.assets, self.board_geo, self.game_state, 
            config.screen, config.width, config.height
        )
        self.controller = GameController(self.board_geo, self.game_state)
        
        if vs_bot:
            self.controller.set_vs_bot(True)
    
    def run(self):
        """Run the game session."""
        clock = pygame.time.Clock()
        
        while True:
            events = pygame.event.get()
            should_exit = self._handle_events(events)
            
            if should_exit is not None:
                return should_exit
            
            self.controller.update()
            self._render_frame()
            
            pygame.display.flip()
            clock.tick(60)
    
    def _handle_events(self, events):
        """Handle pygame events."""
        for event in events:
            if event.type == pygame.QUIT:
                return QUIT_GAME
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return RETURN_TO_MENU
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                point_idx = self.controller.nearest_point(event.pos)
                if point_idx is not None:
                    self.controller.handle_click(point_idx)
        return None
    
    def _render_frame(self):
        """Render a single frame."""
        self.renderer.draw_background()
        self.renderer.draw_frame()
        self.renderer.draw_board()
        self.renderer.draw_available_positions()
        self.renderer.draw_pieces()
        self.renderer.draw_ui()
    
    def cleanup(self):
        """Clean up resources (if needed)."""
        # Clear any cached state in components
        self.controller.set_vs_bot(False)
        