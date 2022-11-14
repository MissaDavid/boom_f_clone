import random
from random import choice

import pygame as py

from base_character import Character
from game_settings import ASSET_FOLDER
from utils import import_sprites, Direction


class Enemy(Character):
    def __init__(self, position: tuple, sprite: py.Surface):
        super().__init__(position, sprite)
        self.all_sprites = import_sprites(f"{ASSET_FOLDER}/tilesets/enemy1.png")
        self.animations = self.set_animation_sprites()
        self.movement_speed = 1.1
        self.animation_speed = 0.4
        self.steps = 0
        self.facing_direction: Direction = Direction.K_LEFT

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

    def set_random_direction(self, x: bool = False, y: bool = False):
        """
        Randomly choose the direction to walk
        """
        pressed = choice(list(Direction))
        if x:
            pressed = choice([Direction.K_LEFT, Direction.K_RIGHT])
        if y:
            pressed = choice([Direction.K_UP, Direction.K_DOWN])

        # reset initial direction to "idle"
        self.direction.x = 0
        self.direction.y = 0

        match pressed:
            case Direction.K_RIGHT:
                self.direction.x = 1
                self.facing_direction = Direction.K_RIGHT
            case Direction.K_LEFT:
                self.direction.x = -1
                self.facing_direction = Direction.K_LEFT
            case Direction.K_DOWN:
                self.direction.y = 1
                self.facing_direction = Direction.K_DOWN
            case Direction.K_UP:
                self.direction.y = -1
                self.facing_direction = Direction.K_UP

    def shoot(self):
        return Bullet((self.rect.x, self.rect.y))

    def update(self, obstacles: list) -> None:
        """
        Enemy movement is a little more complex than the Player's
        The idea is to set a random direction and move the sprite for a random number of steps.
        If there is a collision before the end of the allocated steps,
        then we set a new random direction and a new number of steps.

        :param obstacles: list of all obstacle tiles
        """
        if self.steps == 0:
            self.set_random_direction()
            self.steps = random.randrange(0, 120, step=30)
        else:
            self.animate_walking(self.animations)
            self.steps -= 1
            self.rect.x += self.direction.x * self.movement_speed
            self.rect.y += self.direction.y * self.movement_speed
            match self.facing_direction:
                case Direction.K_LEFT:
                    collision = self.get_collision(obstacles)
                    if collision and collision.rect.right > self.rect.left:
                        self.rect.left = collision.rect.right
                        self.set_random_direction()
                case Direction.K_RIGHT:
                    collision = self.get_collision(obstacles)
                    if collision and collision.rect.left < self.rect.right:
                        self.rect.right = collision.rect.left
                        self.set_random_direction()
                case Direction.K_UP:
                    collision = self.get_collision(obstacles)
                    if collision and collision.rect.bottom > self.rect.top:
                        self.rect.top = collision.rect.bottom
                        self.set_random_direction()
                case Direction.K_DOWN:
                    collision = self.get_collision(obstacles)
                    if collision and collision.rect.top < self.rect.bottom:
                        self.rect.bottom = collision.rect.top
                        self.set_random_direction()


class Bullet(py.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()
        self.all_sprites = import_sprites(f"{ASSET_FOLDER}/tilesets/shot.png")
        self.image = self.all_sprites[0]
        self.rect = self.image.get_rect(center=position)
        self.speed = 5
        self.mask = py.mask.from_surface(self.image)

    def update(self) -> None:
        self.rect.x += 5
