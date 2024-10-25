import pygame
from pytmx.util_pygame import load_pygame

from classes.zombie import Zombie
from classes.player import Player
from constants.globals import WINDOW_SIZE, WINDOW_TITLE
from helpers.createMenu import create_menu

pygame.init()

# Window
display = pygame.display
display.set_caption(WINDOW_TITLE)
screen = display.set_mode(WINDOW_SIZE)

# Create sprite groups
projectile_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()

# Declaring entities
player = Player(640, 360, 3,5)
zombie = Zombie(100, 100, 3, 1, player)

# Main loop
if __name__ == '__main__':
    menu = create_menu(projectile_group, zombie, player, screen)
    menu.mainloop(screen)
