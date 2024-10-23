import pygame
from pytmx.util_pygame import load_pygame

from classes.entity import Entity
from classes.zombie import Zombie
from constants.globals import WINDOW_SIZE, WINDOW_TITLE
from helpers.createMenu import create_menu

pygame.init()

# Window
display = pygame.display
display.set_caption(WINDOW_TITLE)
screen = display.set_mode(WINDOW_SIZE)

# TMX Map data
tmxdata = load_pygame("map/test.tmx")

# Create sprite groups
projectile_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()

# Declaring entities
player = Entity('player', 640, 360, 3, 5)
zombie = Zombie(100, 100, 3, 2, player)
zombie_group.add(zombie)

# Main loop
if __name__ == '__main__':
    menu = create_menu(projectile_group, zombie_group, player, screen)
    menu.mainloop(screen)