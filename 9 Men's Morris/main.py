import pygame
import sys
from constants import setup_screen, COLORS
from game_assets import GameAssets
from board_geometry import BoardGeometry
from game_state import GameState
from game_renderer import GameRenderer
from game_controller import GameController

def main():
    pygame.init()
    
    # Khởi tạo màn hình
    screen, screen_w, screen_h, cx, cy = setup_screen()
    
    # Khởi tạo các component
    assets = GameAssets(screen_w, screen_h, cx, cy)
    board_geo = BoardGeometry(assets.board_half, cx, cy)
    game_state = GameState(board_geo)
    renderer = GameRenderer(assets, board_geo, game_state, screen, screen_w, screen_h)
    controller = GameController(board_geo, game_state)
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                point_idx = controller.nearest_point(event.pos)
                if point_idx is not None:
                    controller.handle_click(point_idx)
        
        # Render
        renderer.draw_background()
        renderer.draw_frame()
        renderer.draw_board()
        renderer.draw_pieces()
        renderer.draw_ui()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()