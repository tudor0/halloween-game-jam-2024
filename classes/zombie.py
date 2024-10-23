import pygame
from classes.entity import Entity
from classes.entity import screen

class Zombie(Entity, pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, target):
        Entity.__init__(self, 'zombie', x, y, scale, speed)  # Use 'player' entity type
        pygame.sprite.Sprite.__init__(self)
        self.target = target  # The player or target entity
        self.aggro_range = 200
        self.range_x = self.rect.x + self.aggro_range
        self.range_y = self.rect.y + self.aggro_range

    def move_towards_target(self):
        # Calculate direction towards the target
        dx = self.target.rect.x - self.rect.x
        dy = self.target.rect.y - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance != 0:
            dx = dx / distance
            dy = dy / distance

        # Move zombie
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Update direction for animation
        if abs(dx) > abs(dy):
            if dx > 0:
                self.update_action(1)  # walking right
                self.flip = False
            else:
                self.update_action(1)  # walking left
                self.flip = True
        else:
            if dy > 0:
                self.update_action(0)  # walking down
            else:
                self.update_action(2)  # walking up

    def check_for_target(self):
        #if self.target.rect.x <= self.range_x or self.target.rect.y <= self.range_y:
           #self.move_towards_target()

        if self.rect.x-self.aggro_range <= self.target.rect.x <= self.rect.x+self.aggro_range:
           self.move_towards_target()

    def debug_zombie(self):
        #pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.range_x, self.range_y, 100, 100))
        pygame.draw.circle(screen, (255, 100, 0), self.rect.center, self.aggro_range)