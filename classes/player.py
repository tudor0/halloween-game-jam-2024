import pygame
from classes.entity import Entity
from constants.globals import WINDOW_SIZE

class Player(Entity, pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        Entity.__init__(self, 'player', x, y, scale, speed)  # Use 'player' entity type
        pygame.sprite.Sprite.__init__(self)
        self.direction_x = 1
        self.direction_y = 1

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

        #Check for collision with window edges
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