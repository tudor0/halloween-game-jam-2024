from random import randint
from math import sqrt
import pygame

from classes.entity import Entity
from classes.entity import screen
from constants.animations import ANIMATION_TYPES
from constants.globals import WINDOW_SIZE

class Zombie(Entity, pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, target):
        Entity.__init__(self, 'zombie', x, y, scale, speed)  # Use 'player' entity type
        pygame.sprite.Sprite.__init__(self)
        self.target = target  # The player or target entity

        # Zombie initialisation characteristics
        self.unaware_aggro_range = 200
        self.chase_aggro_range = 300
        self.wandering_range = 150
        self.wandering_minimum = 100
        self.proximity_range = 35
        self.aggro_speed = speed
        self.wandering_speed = speed*0.65
        self.minimum_wait_time = 1000
        self.maximum_wait_time = 2500
        self.wait_duration = randint(self.minimum_wait_time, self.maximum_wait_time)

        # Initial behaviour
        self.aggro_range = self.unaware_aggro_range
        self.behavior = 'wander'

        self.idle_time = 0
        self.delta_speed = [0, 0]
        self.player_location = [self.target.rect.x, self.target.rect.y]

        self.target_points = [self.rect.x, self.rect.y]
        self.last_known_player_location = [self.rect.x, self.rect.y]
        self.random_points = [
            randint(self.last_known_player_location[0], self.last_known_player_location[0] + self.wandering_range),
            randint(self.last_known_player_location[1], self.last_known_player_location[1] + self.wandering_range),
        ]

    def execute_behavior(self):
        match self.behavior:
            case 'aggro':
                self.aggro_range = self.chase_aggro_range
                self.speed = self.aggro_speed
                self.move()
            case 'wander':
                self.aggro_range = self.unaware_aggro_range
                self.speed = self.wandering_speed
                self.move()
            case 'idle':
                self.aggro_range = self.unaware_aggro_range
                self.wait()
            case _:
                self.aggro_range = self.unaware_aggro_range
                self.wait()

    def move(self):
        # Check if the zombie is in idle mode after reaching a random point
        if self.behavior == 'idle':
            # Check if the wait duration has elapsed
            if pygame.time.get_ticks() - self.idle_time >= self.wait_duration:
                # Exit idle mode and choose a new random point to wander to
                self.behavior = 'wander'
                self.choose_random_point()
                self.target_points = self.random_points
                self.idle_time = 0  # Reset idle time for the next wait
                self.wait_duration = randint(self.minimum_wait_time, self.maximum_wait_time)
            else:
                return  # Stay idle and do nothing

        # If not in idle mode, proceed to choose target and move
        self.choose_target()

        # Calculate direction towards the target
        for i in range(len(self.delta_speed)):
            self.delta_speed[i] = self.target_points[i] - self.rect.center[i]

        distance = sqrt(pow(self.delta_speed[0], 2) + pow(self.delta_speed[1], 2))

        for i in range(len(self.delta_speed)):
            if distance != 0:
                self.delta_speed[i] = self.delta_speed[i] / distance

        # Move towards the target
        self.rect.x += self.delta_speed[0] * self.speed
        self.rect.y += self.delta_speed[1] * self.speed

        # Check if zombie reached target and switch to idle if wandering
        if self.behavior == 'wander' and pygame.math.Vector2(self.rect.center).distance_to(
                self.target_points) < self.proximity_range:
            self.behavior = 'idle'
            self.idle_time = pygame.time.get_ticks()  # Record the time zombie reached the point

        # Update sprite
        self.update_direction()

    def choose_target(self):
        # Update to current player location
        self.player_location = [self.target.rect.x, self.target.rect.y]

        target_distance_from_zombie = int(pygame.math.Vector2(self.player_location).distance_to(self.rect.center))

        # Define target point: player or random
        # Aggro behaviour
        if target_distance_from_zombie <= self.aggro_range:
            self.behavior = 'aggro'
            self.target_points = self.player_location

            for i in range(len(self.last_known_player_location)):
                self.last_known_player_location[i] = self.target_points[i]

            for i in range(len(self.random_points)):
                self.random_points[i] = self.target_points[i]

        else:
            self.behavior = 'wander'
            self.target_points = self.random_points

        if target_distance_from_zombie <= self.proximity_range:
            self.behavior = 'idle'

    def wait(self):
        self.player_location = [self.target.rect.x, self.target.rect.y]

        if self.idle_time == 0:
            self.idle_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.idle_time > self.wait_duration:
            self.behavior = 'wander'
            self.choose_random_point()
            self.idle_time = 0
            self.wait_duration = randint(self.minimum_wait_time, self.maximum_wait_time)

        # Target enters aggro range while waiting
        if pygame.math.Vector2(self.player_location).distance_to(self.rect.center) <= self.aggro_range:
            self.behavior = 'aggro'
            self.idle_time = 0
            self.wait_duration = randint(self.minimum_wait_time, self.maximum_wait_time)

        self.delta_speed = [0 ,0]
        self.update_direction()

    def update_direction(self):
        if self.delta_speed[0] == 0 and self.delta_speed[1] == 0:
            self.update_action('idle')
        if abs(self.delta_speed[0]) > abs(self.delta_speed[1]):
            if self.delta_speed[0] > 0:
                self.update_action(ANIMATION_TYPES['walking_horizontally'])  # walking right
                self.flip = False
            else:
                self.update_action(ANIMATION_TYPES['walking_horizontally'])  # walking left
                self.flip = True
        elif abs(self.delta_speed[0]) < abs(self.delta_speed[1]):
            if self.delta_speed[1] > 0:
                self.update_action(ANIMATION_TYPES['walking_down'])  # walking down
            else:
                self.update_action(ANIMATION_TYPES['walking_up'])  # walking up

    def choose_random_point(self):
        while True:
            for i in range(len(self.last_known_player_location)):
                self.random_points[i] = randint(self.last_known_player_location[i], self.last_known_player_location[i] + self.wandering_range)

                # Stops the zombie from choosing points out of bounds
                if 0 > self.random_points[i] > WINDOW_SIZE[i]:
                    self.random_points[i] = self.rect.center[i]

            distance = pygame.math.Vector2(self.random_points).distance_to(self.rect.center)

            if distance >= self.wandering_minimum:
                break

    def debug_zombie(self):
        pygame.draw.circle(screen, (255, 100, 0), self.rect.center, self.aggro_range) #Aggro range
        pygame.draw.circle(screen, (255, 0, 0), self.random_points, self.proximity_range) #Random chosen point
        print("pygame.time.get_ticks() - self.idle_time")
        print(pygame.time.get_ticks() - self.idle_time)
        print("self.wait_duration")
        print(self.wait_duration)
        print("self.idle_time")
        print(self.idle_time)
        print('self.random_points')
        print(self.random_points)
        print("self.delta_speed")
        print(self.delta_speed)
        print("---------------------------")
