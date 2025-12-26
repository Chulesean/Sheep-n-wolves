import pygame
from constants import COLORS


class MainMenu:
    """
    Represents the main menu of the game, allowing the player
    to choose between game modes or exit the application.
    """

    def __init__(self, screen, screen_w, screen_h):
        """
        Initialize the main menu.

        :param screen: Pygame display surface
        :param screen_w: Screen width
        :param screen_h: Screen height
        """
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.title_font = pygame.font.SysFont(None, 80)
        self.button_font = pygame.font.SysFont(None, 50)

        self.selected_option = 0
        self.options = ["Player vs Player", "Player vs Bot", "Exit"]
        self.button_rects = []

    def draw(self):
        """
        Draw the main menu, including title and selectable buttons.
        """
        self.screen.fill((30, 30, 60))

        title = self.title_font.render(
            "Poddavki Checkers", True, COLORS['WHITE']
        )
        title_rect = title.get_rect(
            center=(self.screen_w // 2, self.screen_h * 0.3)
        )
        self.screen.blit(title, title_rect)

        self.button_rects = []
        for i, option in enumerate(self.options):
            color = (
                COLORS['GREEN']
                if i == self.selected_option
                else COLORS['WHITE']
            )

            text = self.button_font.render(option, True, color)
            text_rect = text.get_rect(
                center=(self.screen_w // 2, self.screen_h * 0.5 + i * 80)
            )

            button_rect = text_rect.inflate(40, 20)

            pygame.draw.rect(
                self.screen,
                COLORS['BLACK'],
                button_rect,
                border_radius=10
            )
            pygame.draw.rect(
                self.screen,
                color,
                button_rect,
                2,
                border_radius=10
            )

            self.screen.blit(text, text_rect)
            self.button_rects.append(button_rect)

    def handle_input(self, events):
        """
        Handle keyboard and mouse input for menu navigation.

        :param events: List of Pygame events
        :return: Selected option index, or None if no selection was made
        """
        mouse_pos = pygame.mouse.get_pos()

        # Highlight button under mouse cursor
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_option = i
                break

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (
                        self.selected_option - 1
                    ) % len(self.options)

                elif event.key == pygame.K_DOWN:
                    self.selected_option = (
                        self.selected_option + 1
                    ) % len(self.options)

                elif event.key == pygame.K_RETURN:
                    return self.selected_option

                elif event.key == pygame.K_ESCAPE:
                    return 2  # Exit option

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        return i

        return None
