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

        self.direction = pygame.math.Vector2(0, 0)
        self.facing_right = False
        self.facing_down = False
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
        """
        The Player's moving direction is a Vector2 representing x, y axis
        0, 0 represents the top left corner SO y axis is a positive in when going DOWN

        x:
            Going right == 1, going left == -1
        y:
            Going down == 1, going up == -1
        """
        key_state = pygame.key.get_pressed()

        self.direction.x = key_state[pygame.K_RIGHT] - key_state[pygame.K_LEFT]
        self.direction.y = key_state[pygame.K_DOWN] - key_state[pygame.K_UP]

        self.facing_right = True if self.direction.x == 1 else False
        self.facing_down = True if self.direction.y == 1 else False

    def move(self):
        x = self.direction.x
        y = self.direction.y

        if x > 0:
            self.image = self.animations["walk_right"][0]
            self.rect.move_ip(x * self.speed, y)
        elif x < 0:
            self.image = self.animations["walk_left"][0]
            self.rect.move_ip(x * self.speed, y)
        elif y > 0:
            self.image = self.animations["walk_down"][0]
            self.rect.move_ip(x, y * self.speed)
        elif y < 0:
            self.image = self.animations["walk_up"][0]
            self.rect.move_ip(x, y * self.speed)
        else:
            self.image = self.animations["idle"]

    def update(self):
        """
        Get key input to set the direction, then move
        """
        self.set_direction()
        self.move()
