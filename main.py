import pygame
from pytmx.util_pygame import load_pygame

from classes.entity import Entity
from constants.globals import WINDOW_WIDTH, WINDOW_SIZE, WINDOW_TITLE, WINDOW_HEIGHT, FRAME_RATE
import os

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

# PROJECTILE CLASS
class Projectile(pygame.sprite.Sprite):
    def __init__(self, projectile_type, x, y, scale, speed, direction):
        self.projectile_type = projectile_type
        self.speed = speed
        self.animation_list = []
        self.frame_index = 0

        # add image lists to array
        # count number of files in the folder
        num_of_frames = len(os.listdir(f'gfx/{self.projectile_type}'))
        temp_list = []
        for i in range(num_of_frames):
            img = pygame.image.load(f'gfx/{self.projectile_type}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction


# TMX Map data
tmxdata = load_pygame("map/test.tmx")

# Create sprite groups
projectile_group = pygame.sprite.Group()

# Declaring entities
player = Entity('player', 640, 360, 3, 5)

# GAME LOOP
while True:

    CLOCK.tick(FRAME_RATE)

    draw_background()

    # update and draw sprite groups
    projectile_group.update()
    projectile_group.draw(screen)

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