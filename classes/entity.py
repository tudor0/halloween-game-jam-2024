import pygame
import os
from constants.globals import WINDOW_SIZE
from constants.animations import ANIMATION_COOLDOWN
from constants.animations import ANIMATION_TYPES

# Window
display = pygame.display
screen = display.set_mode(WINDOW_SIZE)

# ENTITY CLASS
class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.entity_type = entity_type
        self.speed = speed
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Loading animations
        try:
            for animation in ANIMATION_TYPES:
                # reset temp list of images
                temp_list = []
                # count number of files in the folder
                num_of_frames = len(os.listdir(f'gfx/{self.entity_type}/{animation}'))
                # add image lists to array
                for i in range(num_of_frames):
                    img = pygame.image.load(f'gfx/{self.entity_type}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)
        except:
            print('Animation not defined')

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        # update image to current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # if idle, keep facing last position
        if new_action == 'idle':
            self.frame_index = 0
        # check if new action is different to the previous one
        elif new_action != self.action:
            self.action = new_action
            # update the animation from the start
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)