"""
Main menu interface for Nine Men's Morris.

Provides game mode selection with visual menu, hover effects,
and both keyboard/mouse navigation support.
"""

import pygame
from constants import COLORS

class MainMenu:
    """Main menu for Nine Men's Morris game."""
    
    def __init__(self, screen, screen_w, screen_h):
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.title_font = pygame.font.SysFont(None, 80)
        self.button_font = pygame.font.SysFont(None, 50)
        self.selected_option = 0
        self.options = ["Player vs Player", "Player vs Bot", "Exit"]
        self.button_rects = []
        
        # Define colors as constants
        self.BACKGROUND_COLOR = (30, 30, 60)  # Dark blue
        self.BUTTON_COLOR = COLORS['BLACK']
        self.SELECTED_COLOR = COLORS['GREEN']
        self.NORMAL_COLOR = COLORS['WHITE']
        
        # Define layout constants (percentages of screen)
        self.TITLE_Y_POSITION = 0.3  # 30% from top
        self.BUTTON_START_Y = 0.5    # 50% from top
        self.BUTTON_SPACING = 80     # pixels between buttons
        self.BUTTON_PADDING = (60, 25)  # (horizontal, vertical) padding
        
        # Calculate layout once
        self._calculate_layout()
    
    def _calculate_layout(self):
        """Calculate button positions and store in self.button_rects."""
        self.button_rects = []
        
        for i, option in enumerate(self.options):
            # Calculate button position
            button_y = int(self.screen_h * self.BUTTON_START_Y + i * self.BUTTON_SPACING)
            
            # Create text surface to get size
            text_surface = self.button_font.render(option, True, self.NORMAL_COLOR)
            text_rect = text_surface.get_rect(center=(self.screen_w // 2, button_y))
            
            # Inflate for button padding
            button_rect = text_rect.inflate(*self.BUTTON_PADDING)
            self.button_rects.append(button_rect)
    
    def update(self, events):
        """
        Update menu state based on events.
        
        Returns:
            int or None: Selected option index, or None if no selection
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Update hover selection
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_option = i
                break
        
        # Handle input events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.selected_option
                elif event.key == pygame.K_ESCAPE:
                    return 2  # Exit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        return i
        
        return None
    
    def draw(self):
        """Draw the menu (no side effects)."""
        # Clear screen with background color
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Draw title
        title = self.title_font.render("Nine Men's Morris", True, COLORS['WHITE'])
        title_rect = title.get_rect(
            center=(self.screen_w // 2, int(self.screen_h * self.TITLE_Y_POSITION))
        )
        self.screen.blit(title, title_rect)
        
        # Draw buttons
        for i, (option, button_rect) in enumerate(zip(self.options, self.button_rects)):
            # Determine button color based on selection
            color = self.SELECTED_COLOR if i == self.selected_option else self.NORMAL_COLOR
            
            # Render button text
            text = self.button_font.render(option, True, color)
            text_rect = text.get_rect(center=button_rect.center)
            
            # Draw button background
            pygame.draw.rect(self.screen, self.BUTTON_COLOR, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, color, button_rect, 2, border_radius=10)
            
            # Draw button text
            self.screen.blit(text, text_rect)
