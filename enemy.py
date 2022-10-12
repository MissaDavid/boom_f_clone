import pygame as py

from game_settings import ASSET_FOLDER, FPS
from utils import import_sprites


class Character(py.sprite.Sprite):
    def __init__(self):
        super().__init__()


class Enemy(py.sprite.Sprite):
    def __init__(self, position: tuple, sprite):
        super().__init__()
        self.all_sprites = import_sprites(f"{ASSET_FOLDER}/tilesets/enemy1.png")
        self.animations = self.set_animation_sprites()
        self.image = sprite
        self.rect = self.image.get_rect(topleft=position)
        self.direction = py.math.Vector2(0, 0)
        self.face_right = False
        self.face_left = False
        self.face_down = False
        self.face_up = False
        self.movement_speed = 4
        self.frame_index = 0
        self.animation_speed = 0.5
        self.is_hit = False
        self.lose_animation_timer = FPS * 2

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

    def animate(self):
        self.frame_index += self.animation_speed
        if self.direction.x < 0:
            if self.frame_index >= len(self.animations["walk_left"]):
                self.frame_index = 0
            self.image = self.animations["walk_left"][int(self.frame_index)]
        if self.direction.x > 0:
            if self.frame_index >= len(self.animations["walk_right"]):
                self.frame_index = 0
            self.image = self.animations["walk_right"][int(self.frame_index)]
        if self.direction.y > 0:
            if self.frame_index >= len(self.animations["walk_down"]):
                self.frame_index = 0
            self.image = self.animations["walk_down"][int(self.frame_index)]
        elif self.direction.y < 0:
            if self.frame_index >= len(self.animations["walk_up"]):
                self.frame_index = 0
            self.image = self.animations["walk_up"][int(self.frame_index)]

    def move(self):
        """Randomly move left / right / up / down if no obstacles"""
        self.animate()

    def shoot(self):
        ...

    def update(self) -> None:
        ...
