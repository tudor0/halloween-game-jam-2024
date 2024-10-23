import pygame
import os
from constants.globals import WINDOW_SIZE, WINDOW_TITLE
from constants.animations import ANIMATION_COOLDOWN
# Window
display = pygame.display
display.set_caption(WINDOW_TITLE)
screen = display.set_mode(WINDOW_SIZE)

# ENTITY CLASS
class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.entity_type = entity_type
        self.speed = speed
        self.direction_x = 1
        self.direction_y = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Loading animations
        # structure {animation:index}
        animation_types = {'walking_down': 0, 'walking_horizontally': 1, 'walking_up': 2}

        for animation in animation_types:
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

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_up, moving_left, moving_down, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables
        if moving_up:
            dy = -self.speed
            self.direction_y = -1
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction_x = -1
        if moving_down:
            dy = self.speed
            self.direction_y = 1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction_x = 1

        # update rect position with boundary checks
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        if new_x < 0:
            self.rect.x = 0
        elif new_x + self.rect.width > WINDOW_SIZE[0]:
            self.rect.x = WINDOW_SIZE[0] - self.rect.width
        else:
            self.rect.x = new_x

        if new_y < 0:
            self.rect.y = 0
        elif new_y + self.rect.height > WINDOW_SIZE[1]:
            self.rect.y = WINDOW_SIZE[1] - self.rect.height
        else:
            self.rect.y = new_y

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