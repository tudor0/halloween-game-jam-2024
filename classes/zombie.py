import pygame
from classes.entity import Entity
from constants.globals import WINDOW_SIZE, WINDOW_TITLE

# Window
display = pygame.display
display.set_caption(WINDOW_TITLE)
screen = display.set_mode(WINDOW_SIZE)

# Zombie class inheriting from Entity and pygame.sprite.Sprite
class Zombie(Entity, pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, target):
        Entity.__init__(self, 'zombie', x, y, scale, speed)  # Use 'player' entity type
        pygame.sprite.Sprite.__init__(self)
        self.target = target  # The player or target entity

    def update(self):
        # Move towards the target
        self.move_towards_target()
        # Update animation
        self.update_animation()

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