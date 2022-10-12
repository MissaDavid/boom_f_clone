from random import choice

import pygame as py

from base_character import Character
from game_settings import ASSET_FOLDER
from utils import import_sprites


class Enemy(Character):
    def __init__(self, position: tuple, sprite: py.Surface):
        super().__init__(position, sprite)
        self.all_sprites = import_sprites(f"{ASSET_FOLDER}/tilesets/enemy1.png")
        self.animations = self.set_animation_sprites()
        self.face_right = False
        self.face_left = False
        self.face_down = False
        self.face_up = False
        self.movement_speed = 1.2

    def set_animation_sprites(
        self,
    ) -> dict:
        return {
            "walk_down": self.all_sprites[0:4],
            "walk_up": self.all_sprites[4:8],
            "walk_right": self.all_sprites[8:12],
            "walk_left": self.all_sprites[12:16],
            "shoot_down": self.all_sprites[16:17],
            "shoot_up": self.all_sprites[17:18],
            "shoot_right": self.all_sprites[18:19],
            "shoot_left": self.all_sprites[19:20],
            "loser": self.all_sprites[20:],
        }

    def set_direction(self) -> None:
        """
        Randomly choose the direction
        """
        keys = [py.K_LEFT, py.K_RIGHT, py.K_DOWN, py.K_UP]
        pressed = choice(keys)

        self.direction.x = 1 if pressed in [py.K_LEFT, py.K_RIGHT] else 0
        self.direction.y = 1 if pressed in [py.K_DOWN, py.K_UP] else 0

    def shoot(self):
        ...

    def update(self, obstacles: list) -> None:
        self.set_direction()
        self.animate_walking(self.animations)
        self.move(obstacles)
