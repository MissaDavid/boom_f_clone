import pygame as py

from game_settings import FPS


class Character(py.sprite.Sprite):
    def __init__(self, position: tuple, sprite: py.Surface):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect(topleft=position)
        self.direction = py.math.Vector2(0, 0)
        self.movement_speed = 4
        self.frame_index = 0
        self.animation_speed = 0.5
        self.lose_animation_timer = FPS * 2
        self.is_hit = False

    def animate_walking(self, animations: dict, has_idle_state: bool = False):
        if has_idle_state:
            if self.direction == [0, 0]:
                self.image = animations["idle"]

        self.frame_index += self.animation_speed
        if self.direction.x < 0:
            if self.frame_index >= len(animations["walk_left"]):
                self.frame_index = 0
            self.image = animations["walk_left"][int(self.frame_index)]
        if self.direction.x > 0:
            if self.frame_index >= len(animations["walk_right"]):
                self.frame_index = 0
            self.image = animations["walk_right"][int(self.frame_index)]
        if self.direction.y > 0:
            if self.frame_index >= len(animations["walk_down"]):
                self.frame_index = 0
            self.image = animations["walk_down"][int(self.frame_index)]
        elif self.direction.y < 0:
            if self.frame_index >= len(animations["walk_up"]):
                self.frame_index = 0
            self.image = animations["walk_up"][int(self.frame_index)]

    def get_collision(self, obstacles):
        for sprite in obstacles:
            if self.rect.colliderect(sprite):
                return sprite

    def move(self, obstacles) -> None:
        """
        Move the character's rect
        Check for a potential collision on each axis

        :param obstacles: list of all obstacle tiles
        """
        if self.direction.x != 0:
            self.rect.x += self.direction.x * self.movement_speed
            collision = self.get_collision(obstacles)
            if collision:
                if self.direction.x < 0:
                    self.rect.left = collision.rect.right
                elif self.direction.x > 0:
                    self.rect.right = collision.rect.left

        if self.direction.y != 0:
            self.rect.y += self.direction.y * self.movement_speed
            collision = self.get_collision(obstacles)
            if collision:
                if self.direction.y > 0:
                    self.rect.bottom = collision.rect.top
                elif self.direction.y < 0:
                    self.rect.top = collision.rect.bottom
