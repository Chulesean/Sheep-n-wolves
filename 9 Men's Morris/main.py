"""
Main entry point and game loop for Nine Men's Morris.

Initializes game components, manages main loop, handles transitions
between menu and gameplay, and coordinates all subsystems.
"""

import pygame
import sys
import traceback
from constants import setup_screen, ScreenConfig, RETURN_TO_MENU, QUIT_GAME
from menu import MainMenu
from game_session import GameSession

def run_game(config: ScreenConfig, vs_bot: bool = False):
    """
    Run a game session.
    
    Args:
        config: Screen configuration
        vs_bot: Whether playing against bot
        
    Returns:
        RETURN_TO_MENU: Return to main menu
        QUIT_GAME: Exit the game
    """
    session = GameSession(config, vs_bot)
    try:
        return session.run()
    finally:
        session.cleanup()

def main():
    """Main entry point."""
    pygame.init()
    
    try:
        # Get screen configuration
        config = setup_screen()
        
        # Create main menu
        menu = MainMenu(config.screen, config.width, config.height)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            # Update menu and get selection
            selected_option = menu.update(events)
            menu.draw()
            pygame.display.flip()
            
            # Handle menu selection
            if selected_option is not None:
                if selected_option == 0:  # Player vs Player
                    result = run_game(config, False)
                    if result == QUIT_GAME:
                        running = False
                    # If RETURN_TO_MENU, continue loop
                    
                elif selected_option == 1:  # Player vs Bot
                    result = run_game(config, True)
                    if result == QUIT_GAME:
                        running = False
                    # If RETURN_TO_MENU, continue loop
                    
                elif selected_option == 2:  # Exit
                    running = False
            
            clock.tick(60)
            
    except Exception as e:
        print(f"Fatal error in game: {e}")
        traceback.print_exc()
        
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
    
