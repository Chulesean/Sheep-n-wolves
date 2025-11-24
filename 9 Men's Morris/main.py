import pygame
import sys
from constants import setup_screen
from game_assets import GameAssets
from board_geometry import BoardGeometry
from game_state import GameState
from game_renderer import GameRenderer
from game_controller import GameController
from menu import MainMenu
from bot import NineMensMorrisBot

def run_game(screen, screen_w, screen_h, cx, cy, vs_bot=False):
    assets = GameAssets(screen_w, screen_h, cx, cy)
    board_geo = BoardGeometry(assets.board_half, cx, cy)
    game_state = GameState(board_geo)
    renderer = GameRenderer(assets, board_geo, game_state, screen, screen_w, screen_h)
    controller = GameController(board_geo, game_state)
    
    if vs_bot:
        controller.set_vs_bot(True)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True  # Quay lại menu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                point_idx = controller.nearest_point(event.pos)
                if point_idx is not None:
                    controller.handle_click(point_idx)
        
        controller.update()
        
        renderer.draw_background()
        renderer.draw_frame()
        renderer.draw_board()
        renderer.draw_available_positions()
        renderer.draw_pieces()
        renderer.draw_ui()
        
        pygame.display.flip()
        clock.tick(60)
    
    return False

def main():
    pygame.init()
    
    screen, screen_w, screen_h, cx, cy = setup_screen()
    menu = MainMenu(screen, screen_w, screen_h)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        selected = menu.handle_input(events)
        menu.draw()
        pygame.display.flip()
        
        if selected is not None:
            if selected == 0:  # Player vs Player
                continue_game = run_game(screen, screen_w, screen_h, cx, cy, False)
                if not continue_game:
                    running = False
            elif selected == 1:  # Player vs Bot
                continue_game = run_game(screen, screen_w, screen_h, cx, cy, True)
                if not continue_game:
                    running = False
            elif selected == 2:  # Exit
                running = False
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
