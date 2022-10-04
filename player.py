import pygame as py

from game_settings import ASSET_FOLDER, FPS
from utils import import_sprites


class Player(py.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()
        self.all_sprites = import_sprites(f"{ASSET_FOLDER}/tilesets/player_one.png")
        self.animations = self.set_animation_sprites()
        self.image: py.Surface = self.animations["idle"]
        self.rect = self.image.get_rect(topleft=position)
        self.direction = py.math.Vector2(0, 0)
        # self.face_right = False
        # self.face_left = False
        # self.face_down = False
        # self.face_up = False
        self.movement_speed = 4
        self.frame_index = 0
        self.animation_speed = 0.5
        self.has_triggered_bomb = False
        self.is_hit = False
        self.life_points = 8
        self.invincibility_timer = FPS
        self.lose_animation_timer = FPS * 2

    def set_animation_sprites(
        self,
    ) -> dict:
        return {
            "idle": self.all_sprites[0],
            "walk_down": self.all_sprites[1:8],
            "walk_up": self.all_sprites[8:16],
            "walk_right": self.all_sprites[16:24],
            "walk_left": self.all_sprites[24:32],
            "loser": self.all_sprites[32:35],
            "winner": self.all_sprites[35:],
        }

    def set_direction(self) -> None:
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

        # self.face_right = True if self.direction.x == 1 else False
        # self.face_left = True if self.direction.x == -1 else False
        # self.face_up = True if self.direction.y == -1 else False
        # self.face_down = True if self.direction.y == 1 else False

    def remove_life_points(self, hit_points) -> None:
        """
        a Player has 8 life points at the start of the game
        :param hit_points: number of life points to remove
        """
        if self.life_points > 0:
            self.life_points -= hit_points

    def animate(self):
        if self.direction == [0, 0]:
            self.image = self.animations["idle"]

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

    def get_collisions(self, obstacles):
        collisions = []
        for sprite in obstacles:
            if self.rect.colliderect(sprite):
                collisions.append(sprite)

        return collisions

    def move(self, obstacles):
        self.animate()

        self.rect.x += self.direction.x * self.movement_speed
        collisions = self.get_collisions(obstacles)
        for tile in collisions:
            if self.direction.x < 0:
                self.rect.left = tile.rect.right
            elif self.direction.x > 0:
                self.rect.right = tile.rect.left

        self.rect.y += self.direction.y * self.movement_speed
        collisions = self.get_collisions(obstacles)
        for tile in collisions:
            if self.direction.y > 0:
                self.rect.bottom = tile.rect.top
            elif self.direction.y < 0:
                self.rect.top = tile.rect.bottom

    def set_bomb(self):
        key_state = py.key.get_pressed()

        if key_state[py.K_SPACE]:
            print("SPACE PRESSED")
            self.has_triggered_bomb = True

    def temp_invincibility(self):
        if self.invincibility_timer == 0:
            self.invincibility_timer = FPS
            self.is_hit = False
        else:
            self.invincibility_timer -= 1

    def death_animation(self):
        if self.lose_animation_timer == 0:
            return

        self.lose_animation_timer -= 1
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations["loser"]):
            self.frame_index = 0
        self.image = self.animations["loser"][int(self.frame_index)]

    def update(self, obstacles: list):
        """
        Get key input to set the direction, then move
        """
        if self.life_points == 0:
            self.death_animation()
        else:
            if self.is_hit:
                self.temp_invincibility()
            self.set_direction()
            self.set_bomb()
            self.move(obstacles)
