import pygame as py

from game_settings import ASSET_FOLDER, TILE_SIZE
from utils import import_sprites


class Player(py.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()
        self.all_sprites = import_sprites(f"{ASSET_FOLDER}/tilesets/player_one.png")
        self.animations = self.set_animation_sprites()
        self.image: py.Surface = self.animations["idle"]
        self.rect = py.Rect(position[0], position[1], TILE_SIZE - 4, TILE_SIZE - 4)
        self.direction = py.math.Vector2(0, 0)
        self.face_right = False
        self.face_left = False
        self.face_down = False
        self.face_up = False
        self.speed = 2

    def set_animation_sprites(
        self,
    ) -> dict:
        return {
            "idle": self.all_sprites[0],
            "walk_down": self.all_sprites[1:7],
            "walk_up": self.all_sprites[8:15],
            "walk_right": self.all_sprites[16:23],
            "walk_left": self.all_sprites[24:31],
            "loser": self.all_sprites[32:34],
            "winner": self.all_sprites[35:],
        }

    def set_direction(self):
        """
        The Player's moving direction is a Vector2 representing x, y axis
        0, 0 represents the top left corner SO y axis is positive when going DOWN

        x:
            Going right == 1, going left == -1
        y:
            Going down == 1, going up == -1
        """
        key_state = py.key.get_pressed()

        self.direction.x = key_state[py.K_RIGHT] - key_state[py.K_LEFT]
        self.direction.y = key_state[py.K_DOWN] - key_state[py.K_UP]

        self.face_right = True if self.direction.x == 1 else False
        self.face_left = True if self.direction.x == -1 else False
        self.face_up = True if self.direction.y == -1 else False
        self.face_down = True if self.direction.y == 1 else False

    def get_collisions(self, obstacles):
        collisions = []
        for sprite in obstacles:
            if self.rect.colliderect(sprite):
                collisions.append(sprite)

        return collisions

    def stop(self):
        self.image = self.animations["idle"]

    def move(self, obstacles):
        if self.direction == [0, 0]:
            self.stop()
            return

        self.rect.x += self.direction.x * self.speed
        collisions = self.get_collisions(obstacles)
        for tile in collisions:
            if self.direction.x < 0:
                self.image = self.animations["walk_left"][0]
                self.rect.left = tile.rect.right
            elif self.direction.x > 0:
                self.image = self.animations["walk_right"][0]
                self.rect.right = tile.rect.left

        self.rect.y += self.direction.y * self.speed
        collisions = self.get_collisions(obstacles)
        for tile in collisions:
            if self.direction.y > 0:
                self.image = self.animations["walk_down"][0]
                self.rect.bottom = tile.rect.top
            elif self.direction.y < 0:
                self.image = self.animations["walk_up"][0]
                self.rect.top = tile.rect.bottom

    def update(self, obstacles: list):
        """
        Get key input to set the direction, then move
        """
        self.set_direction()
        self.move(obstacles)
