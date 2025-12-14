import pygame
import sys
from constants import setup_screen
from assets import GameAssets
from board import Board
from game_state import GameState
from renderer import GameRenderer
from controller import GameController
from menu import MainMenu
from bot import PoddavkiBot

def run_game(screen, screen_w, screen_h, cx, cy, vs_bot=False):
    assets = GameAssets(screen_w, screen_h, cx, cy)
    board = Board()
    game_state = GameState(board)
    renderer = GameRenderer(assets, board, game_state, screen, screen_w, screen_h)
    controller = GameController(assets, board, game_state)
    
    if vs_bot:
        controller.set_vs_bot(True)
        bot = PoddavkiBot("SUICIDE")
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                result = controller.handle_keydown(event)
                if result == 'exit':
                    return True  
                elif result == 'reset':
                    board = Board()
                    game_state = GameState(board)
                    renderer = GameRenderer(assets, board, game_state, screen, screen_w, screen_h)
                    controller = GameController(assets, board, game_state)
                    if vs_bot:
                        controller.set_vs_bot(True)
                        bot = PoddavkiBot("SUICIDE")
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                controller.handle_click(event.pos)
        
  
        if vs_bot and game_state.turn == 'black' and not game_state.game_over:
            move = bot.get_move(game_state)
            if move:
                src, dst = move
 
                game_state.select(src[0], src[1])
     
                game_state.select(dst[0], dst[1])
        

        renderer.draw_background()
        renderer.draw_frame()
        renderer.draw_board()
        renderer.draw_valid_moves()
        renderer.draw_pieces()
        renderer.draw_ui()
        
        pygame.display.flip()
        clock.tick(60)
    
    return False

def main():
    pygame.init()
    
    screen, screen_w, screen_h, cx, cy = setup_screen(fullscreen=False)
    
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
            if selected == 0: 
                continue_game = run_game(screen, screen_w, screen_h, cx, cy, False)
                if not continue_game:
                    running = False
            elif selected == 1: 
                continue_game = run_game(screen, screen_w, screen_h, cx, cy, True)
                if not continue_game:
                    running = False
            elif selected == 2:  
                running = False
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()