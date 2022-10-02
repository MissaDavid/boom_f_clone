import pygame as py

from game_settings import FPS, ASSET_FOLDER, TILE_SIZE
from tile import Tile
from utils import import_sprites, rect_has_collision


class Bomb(py.sprite.Sprite):
    """
    A bomb set by the Player !
    A standard bomb affects two tiles on each side (`self.explosion_length`)
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
        self.explosion_length = 2
        self.has_exploded = False
        self.frame_index = 0
        self.bomb_animation_speed = 0.5
        self.explosion_animation_speed = 0.75
        self.explosion_group = py.sprite.Group()

    def set_animation_sprites(
        self,
    ) -> dict:
        return {
            "step_one": self.bomb_sprites[0:2],
            "step_two": self.bomb_sprites[1:],
            "explosion": self.explosion_sprites[0:4],
            "single_line": self.explosion_sprites[8:],
        }

    def animate_explosions(self):
        if self.explosion_duration == 0:
            self.has_exploded = True
            return

        self.explosion_duration -= FPS / len(self.animations["explosion"])
        self.frame_index += self.explosion_animation_speed
        self.image = self.animations["explosion"][int(self.frame_index)]
        for e in self.explosion_group.sprites():
            if e.direction == "up" or e.direction == "down":
                sprite = py.transform.rotate(
                    self.animations["single_line"][int(self.frame_index)], 90
                )
            else:
                sprite = self.animations["single_line"][int(self.frame_index)]
            e.image = sprite
        self.explosion_group.draw(py.display.get_surface())

    def spawn_explosions(self, obstacles):
        """
        For each direction, create Rects for the whole length of the explosion
        then check if this would collide with any obstacles (breakable or not)
        If it does not collide with anything, create an Explosion sprite
        Add all the valid sprites to a Group
        """
        if not len(self.explosion_group.sprites()):
            explosions = {"left": [], "right": [], "up": [], "down": []}
            for index in range(self.explosion_length):
                size = (TILE_SIZE, TILE_SIZE)
                index += 1
                explosions["left"].append(
                    py.Rect((self.rect.x - (TILE_SIZE * index), self.rect.y), size)
                )
                explosions["right"].append(
                    py.Rect((self.rect.x + (TILE_SIZE * index), self.rect.y), size)
                )
                explosions["up"].append(
                    py.Rect((self.rect.x, self.rect.y - (TILE_SIZE * index)), size)
                )
                explosions["down"].append(
                    py.Rect((self.rect.x, self.rect.y + (TILE_SIZE * index)), size)
                )

            for direction, values in explosions.items():
                for index, rect in enumerate(values):
                    if rect_has_collision(rect, obstacles) and index == 0:
                        # cannot explode in that direction at all, so don't check the next Rect
                        break
                    elif not rect_has_collision(rect, obstacles):
                        # otherwise, if no collision, create Explosion
                        self.explosion_group.add(
                            Explosion(
                                (rect.x, rect.y),
                                self.animations["single_line"][0],
                                direction,
                            )
                        )

            print(f"EXPLOSION GROUP LENGTH: {len(self.explosion_group)}")

    def explode(self, obstacles: list[py.sprite.Group]):
        if self.has_exploded:
            self.kill()
        elif self.bomb_timer == 0:
            self.spawn_explosions(obstacles)
            self.animate_explosions()
        else:
            self.bomb_timer -= 1
            self.frame_index += self.bomb_animation_speed
            if self.frame_index >= 2:
                self.frame_index = 0
            if self.bomb_timer <= FPS:
                self.image = self.animations["step_two"][int(self.frame_index)]
            else:
                self.image = self.animations["step_one"][int(self.frame_index)]

    def update(self, all_obstacles: list[py.sprite.Group]):
        self.explode(all_obstacles)


class Explosion(Tile):
    def __init__(self, position: tuple, sprite, direction: str):
        super().__init__(position, sprite)
        self.direction = direction
