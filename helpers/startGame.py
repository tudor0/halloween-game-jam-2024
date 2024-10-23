import pygame
from helpers.drawBackground import draw_background
from constants.globals import FRAME_RATE
from constants.animations import ANIMATION_TYPES

# Clock
CLOCK = pygame.time.Clock()

# Player actions
moving_left = False
moving_right = False
moving_up = False
moving_down = False


def start_game(projectile_group, zombie, player, screen):
    global moving_left, moving_right, moving_up, moving_down

    while True:
        CLOCK.tick(FRAME_RATE)

        draw_background(screen)

        # update and draw sprite groups
        projectile_group.update()
        projectile_group.draw(screen)

        zombie.act()
        zombie.update_animation()
        zombie.debug_zombie()
        zombie.draw()

        player.update_animation()
        player.draw()

        # update animation
        if player.alive:
            if moving_down:
                player.update_action(ANIMATION_TYPES['walking_down'])
            elif moving_right or moving_left:
                player.update_action(ANIMATION_TYPES['walking_horizontally'])
            elif moving_up:
                player.update_action(ANIMATION_TYPES['walking_up'])
            else:
                player.update_action('idle')
            player.move(moving_up, moving_left, moving_down, moving_right)

        # CHECK FOR EVENTS
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
                    exit()
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

        pygame.display.update()