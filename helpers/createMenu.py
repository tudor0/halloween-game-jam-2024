import pygame_menu
from constants.globals import WINDOW_WIDTH, WINDOW_HEIGHT
from helpers.startGame import start_game

def create_menu(projectile_group, zombie_group, player, screen):
    # Create a custom theme
    custom_theme = pygame_menu.themes.THEME_DARK.copy()
    custom_theme.title_font = pygame_menu.font.FONT_FRANCHISE
    custom_theme.widget_font = pygame_menu.font.FONT_FRANCHISE
    custom_theme.title_background_color = (0, 0, 0)  # Pink
    custom_theme.widget_font_color = (255, 255, 255)  # White
    custom_theme.title_font_color = (255, 255, 255)  # White
    custom_theme.widget_background_color = (0, 0, 0)  # Pink

    # Create the menu
    menu = pygame_menu.Menu('Main Menu', WINDOW_WIDTH, WINDOW_HEIGHT, theme=custom_theme)

    # Add buttons to the menu
    menu.add.button('Play', lambda: start_game(projectile_group, zombie_group, player, screen))
    menu.add.button('Quit', pygame_menu.events.EXIT)

    return menu