import pygame as py

from game_settings import FPS, ASSET_FOLDER, TILE_SIZE
from utils import import_sprites


class Bomb(py.sprite.Sprite):
    """
    A bomb set by the Player !
    A standard bomb affects two tiles on each side (`self.dispersion`)
    """

    def __init__(self, position: tuple):
        super().__init__()
        self.bomb_sprites = import_sprites(f"{ASSET_FOLDER}/tilesets/bomb.png")
        self.explosion_sprites = import_sprites(
            f"{ASSET_FOLDER}/tilesets/explosion.png"
        )
        self.animations = self.set_animation_sprites()
        self.image: py.Surface = self.bomb_sprites[0]
        self.rect = self.image.get_rect(topleft=position)
        self.bomb_timer = 4 * FPS  # 4 secs
        self.explosion_duration = FPS  # 1 sec
        self.dispersion = 2
        self.has_exploded = False
        self.frame_index = 0
        self.bomb_animation_speed = 0.5
        self.explosion_animation_speed = 0.75

    def set_animation_sprites(
        self,
    ) -> dict:
        return {
            "step_one": self.bomb_sprites[0:2],
            "step_two": self.bomb_sprites[1:],
            "explosion": self.explosion_sprites[0:4],
        }

    def animate_explosion(self):
        if self.explosion_duration == 0:
            self.has_exploded = True
        else:
            self.explosion_duration -= FPS / len(self.animations["explosion"])
            self.frame_index += self.explosion_animation_speed
            self.image = self.animations["explosion"][int(self.frame_index)]

    def explode(self):
        if self.has_exploded:
            self.kill()
            self.has_exploded = False
        elif self.bomb_timer == 0:
            self.animate_explosion()
        else:
            self.bomb_timer -= 1
            self.frame_index += self.bomb_animation_speed
            if self.frame_index >= 2:
                self.frame_index = 0
            if self.bomb_timer <= FPS:
                self.image = self.animations["step_two"][int(self.frame_index)]
            else:
                self.image = self.animations["step_one"][int(self.frame_index)]

    def update(self):
        self.explode()


class Dispersion(py.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()
        self.rect = py.Rect(position, (TILE_SIZE, TILE_SIZE))
