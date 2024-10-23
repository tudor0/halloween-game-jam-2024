import pygame
import os

# PROJECTILE CLASS
class Projectile(pygame.sprite.Sprite):
    def __init__(self, projectile_type, x, y, scale, speed, direction):
        pygame.sprite.Sprite.__init__(self)
        self.projectile_type = projectile_type
        self.speed = speed
        self.animation_list = []
        self.frame_index = 0

        # add image lists to array
        # count number of files in the folder
        num_of_frames = len(os.listdir(f'gfx/{self.projectile_type}'))
        temp_list = []
        for i in range(num_of_frames):
            img = pygame.image.load(f'gfx/{self.projectile_type}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction