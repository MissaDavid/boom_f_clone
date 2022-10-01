import pygame

from game_settings import ASSET_FOLDER, FPS
from utils import import_sprites


class Tile(pygame.sprite.Sprite):
    """
    A basic Tile with (x,y) coordinates and an optional Sprite
    """

    def __init__(self, position: tuple, sprite):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect(topleft=position)


class Interactive(Tile):
    def __init__(self, position: tuple, sprite):
        super().__init__(position, sprite)
        self.all_sprites = import_sprites(f"{ASSET_FOLDER}/tilesets/breakable.png")
        self.animations = self.set_animation_sprites()
        self.break_animation_speed = 0.75
        self.frame_index = 0
        self.break_duration = FPS
        self.start_timer = 4 * FPS  # start breaking after 4 secs
        self.is_broken = False

    def set_animation_sprites(self) -> dict:
        return {"level_one": self.all_sprites[:4]}

    def breaking_animation(self):
        if self.break_duration == 0:
            self.is_broken = True
        else:
            self.break_duration -= FPS / len(self.animations["level_one"])
            self.frame_index += self.break_animation_speed
            self.image = self.animations["level_one"][int(self.frame_index)]

    def breaks(self):
        if self.is_broken:
            self.kill()

        if self.start_timer == 0:
            self.breaking_animation()
        else:
            self.start_timer -= 1

    def update(self):
        """A breakable tile will start the destruction process when the explosion animation
        of a bomb is almost over
        """
        self.breaks()
