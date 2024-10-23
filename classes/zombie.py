from random import randint, choice

import pygame
from pygame.examples.go_over_there import target_position

from classes.entity import Entity
from classes.entity import screen
from constants.animations import ANIMATION_TYPES
from constants.globals import WINDOW_HEIGHT, WINDOW_WIDTH

class Zombie(Entity, pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, target):
        Entity.__init__(self, 'zombie', x, y, scale, speed)  # Use 'player' entity type
        pygame.sprite.Sprite.__init__(self)
        self.target = target  # The player or target entity
        self.x = x
        self.y = y
        self.aggro_range = 200
        self.wandering_range = 150
        self.choose_random_point()
        self.dx = 0
        self.dy = 0
        self.random_x = 0
        self.random_y = 0
        self.aggro_speed = speed
        self.wandering_speed = self.aggro_speed*0.65
        self.case = 'wander'
        self.idle_time = 0
        self.wait_duration = randint(1000, 2500)

    def move(self):
        #Define target point: player or random
        if pygame.math.Vector2(self.target.rect.x, self.target.rect.y).distance_to((self.rect.x, self.rect.y)) <= self.aggro_range:
            target_x = self.target.rect.x
            target_y = self.target.rect.y
            self.case = 'aggro'
        else:
            target_x = self.random_x
            target_y = self.random_y
            self.case = 'wander'

        if pygame.math.Vector2(self.random_x, self.random_y).distance_to((self.rect.x, self.rect.y)) <= 35:
            self.case = 'idle'

        # Calculate direction towards the target
        self.dx = target_x - self.rect.x
        self.dy = target_y - self.rect.y
        distance = (self.dx ** 2 + self.dy ** 2) ** 0.5

        if distance != 0:
           self.dx = self.dx / distance
           self.dy = self.dy / distance

        # Move zombie
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        #Update_sprite
        self.update_direction()

    def wait(self):
        if self.idle_time == 0:
            self.idle_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.idle_time > self.wait_duration:
            self.case = 'wander'
            self.choose_random_point()
            self.idle_time = 0
            self.wait_duration = randint(1000, 2500)

        if pygame.math.Vector2(self.target.rect.x, self.target.rect.y).distance_to((self.rect.x, self.rect.y)) <= self.aggro_range:
            self.case = 'aggro'
            self.choose_random_point()
            self.idle_time = 0
            self.wait_duration = randint(1000, 2500)

        self.dx = 0
        self.dy = 0

        self.update_direction()

    def update_direction(self):
        if self.dx == 0 and self.dy == 0:
            self.update_action('idle')
        if abs(self.dx) > abs(self.dy):
            if self.dx > 0:
                self.update_action(ANIMATION_TYPES['walking_horizontally'])  # walking right
                self.flip = False
            else:
                self.update_action(ANIMATION_TYPES['walking_horizontally'])  # walking left
                self.flip = True
        elif abs(self.dx) < abs(self.dy):
            if self.dy > 0:
                self.update_action(ANIMATION_TYPES['walking_down'])  # walking down
            else:
                self.update_action(ANIMATION_TYPES['walking_up'])  # walking up

    def choose_random_point(self):
        self.random_x = choice([-1, 1])*randint(self.x, self.x + self.wandering_range)
        self.random_y = choice([-1, 1])*randint(self.y, self.y + self.wandering_range)

        if self.random_x < 0 or self.random_x > WINDOW_WIDTH:
            self.random_x = 0
        if self.random_y < 0 or self.random_y > WINDOW_HEIGHT:
            self.random_y = 0

    def act(self):
        match self.case:
            case 'aggro':
                self.aggro_range = 300
                self.speed = self.aggro_speed
                self.move()
            case 'wander':
                self.aggro_range = 200
                self.speed = self.wandering_speed
                self.move()
            case 'idle':
                self.aggro_range = 200
                self.wait()

    def debug_zombie(self):
        pygame.draw.circle(screen, (255, 100, 0), self.rect.center, self.aggro_range) #Aggro range
        pygame.draw.circle(screen, (255, 0, 0), (self.random_x,self.random_y), 35) #Random chosen point