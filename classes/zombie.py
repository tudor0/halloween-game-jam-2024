from random import randint

import pygame
from classes.entity import Entity
from classes.entity import screen
from constants.globals import WINDOW_HEIGHT, WINDOW_WIDTH

class Zombie(Entity, pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, target):
        Entity.__init__(self, 'zombie', x, y, scale, speed)  # Use 'player' entity type
        pygame.sprite.Sprite.__init__(self)
        self.target = target  # The player or target entity
        self.aggro_range = 200
        self.choose_random_point()
        self.dx = 0
        self.dy = 0

    def move_towards_target(self):
        # Calculate direction towards the target
        self.dx = self.target.rect.x - self.rect.x
        self.dy = self.target.rect.y - self.rect.y
        distance = (self.dx ** 2 + self.dy ** 2) ** 0.5

        if distance != 0:
           self.dx = self.dx / distance
           self.dy = self.dy / distance

        # Move zombie
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        '''# Update direction for animation
        if abs(dx) > abs(dy):
            if dx > 0:
                self.update_action(1)  # walking right
                self.flip = False
            else:
                self.update_action(1)  # walking left
                self.flip = True
        elif abs(dx) < abs(dy):
            if dy > 0:
                self.update_action(0)  # walking down
            else:
                self.update_action(2)  # walking up '''

        self.update_animation()
        self.update_action(2)

    def move_randomly(self):

        self.dx = self.random_x - self.rect.x
        self.dy = self.random_y - self.rect.y
        distance = (self.dx ** 2 + self.dy ** 2) ** 0.5

        if distance != 0:
           self.dx = self.dx / distance
           self.dy = self.dy / distance

        # Move zombie
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        self.update_animation()
        self.update_action(1)

    def choose_random_point(self):
        self.random_x = randint(0, WINDOW_WIDTH)
        self.random_y = randint(0, WINDOW_HEIGHT)

    def check_for_target(self):
        if pygame.math.Vector2(self.target.rect.x, self.target.rect.y).distance_to((self.rect.x, self.rect.y)) <= self.aggro_range:
            self.aggro_range = 300
            self.move_towards_target()
        elif pygame.math.Vector2(self.random_x, self.random_y).distance_to((self.rect.x, self.rect.y)) >= 5:
            self.aggro_range = 200
            self.move_randomly()
        else:
            self.choose_random_point()

    def debug_zombie(self):
        pygame.draw.circle(screen, (255, 100, 0), self.rect.center, self.aggro_range)