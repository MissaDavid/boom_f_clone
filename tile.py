import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, position: tuple, sprite):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect(topleft=position)