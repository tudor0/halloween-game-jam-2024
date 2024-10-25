import pygame

class Sound:
    def __init__(self, sound):
        self.sound = pygame.mixer.Sound(sound)

    def play(self):
        self.sound.play()

    def stop(self):
        self.sound.stop()

    def set_volume(self, volume):
        # Volume level from 0.0 to 1.0
        self.sound.set_volume(volume)

class Music:
    def __init__(self, music):
        self.music = music

    def play(self, loop = -1):
        # Number of loops (-1 means infinite)
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(loop)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def set_volume(self, volume):
        # Volume level from 0.0 to 1.0
        pygame.mixer.music.set_volume(volume)