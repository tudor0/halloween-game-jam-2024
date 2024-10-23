import pygame
from pytmx.util_pygame import load_pygame

from classes.entity import Entity
from classes.player import Player
from classes.zombie import Zombie
from constants.globals import WINDOW_WIDTH, WINDOW_SIZE, WINDOW_TITLE, WINDOW_HEIGHT, FRAME_RATE

pygame.init()

# Window
display = pygame.display
display.set_caption(WINDOW_TITLE)
screen = display.set_mode(WINDOW_SIZE)

# Backgrounds
GRASS_GREEN = (16, 120, 38)


def draw_background():
    screen.fill(GRASS_GREEN)


# Clock
CLOCK = pygame.time.Clock()

# Player actions
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# TMX Map data
tmxdata = load_pygame("map/test.tmx")

# Create sprite groups
projectile_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()

# Declaring entities
player = Player(640, 360, 3,4)
zombie = Zombie(100, 100, 3, 3, player)

# GAME LOOP
while True:

    CLOCK.tick(FRAME_RATE)

    draw_background()

    # update and draw sprite groups
    projectile_group.update()
    projectile_group.draw(screen)

    zombie.update_animation()
    zombie.check_for_target()
    zombie.debug_zombie()
    zombie.draw()

    player.update_animation()
    player.draw()

    # update animation
    if player.alive:
        if moving_down:
            player.update_action(0)
        elif moving_right or moving_left:
            player.update_action(1)
        elif moving_up:
            player.update_action(2)
        else:
            player.update_action('idle')
        player.move(moving_up, moving_left, moving_down, moving_right)

    # CHECK FOR EVENTS
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            pygame.quit()
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        # mouse presses
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left mouse button
            shoot = True

        # keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
        # mouse released
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # left mouse button
            shoot = False

    display.update()