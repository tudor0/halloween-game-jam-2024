import pygame
from classes.entity import Entity

class Player(Entity, pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        Entity.__init__(self, 'player', x, y, scale, speed)  # Use 'player' entity type
        pygame.sprite.Sprite.__init__(self)