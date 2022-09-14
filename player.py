import pygame

from game_settings import ASSET_FOLDER
from utils import import_sprites


class Player(pygame.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()
        self.position = position
        self.spritesheet = import_sprites(f"{ASSET_FOLDER}/tilesets/player_one.png")
        self.animations = self.set_animation_sprites()
        self.image = self.animations["idle"]
        self.rect = self.image.get_rect(topleft=position)

        # Vector2 is a list that contains (x, y) values
        self.direction = pygame.math.Vector2(position)
        self.speed = 4

    def set_animation_sprites(
        self,
    ) -> dict:
        return {
            "idle": self.spritesheet[0],
            "walk_down": self.spritesheet[1:7],
            "walk_up": self.spritesheet[8:15],
            "walk_right": self.spritesheet[16:23],
            "walk_left": self.spritesheet[24:31],
            "loser": self.spritesheet[32:34],
            "winner": self.spritesheet[35:],
        }

    def set_direction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.KEYUP]:
            self.direction.y = 1
        elif keys[pygame.KEYDOWN]:
            self.direction.y = -1

    def move(self):
        pass

    def update(self):
        self.set_direction()
        self.move()
