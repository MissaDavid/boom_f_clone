import os

import pygame

from game_settings import TILE_SIZE
from tile import Tile
from utils import import_csv_layout, import_sprites

TOP_LEVEL_DIR = os.path.join(os.getcwd())


class Level:
    """
    Manages all sprites that are drawn on the display surface
    """

    def __init__(self, level_data: dict):
        # get display surface from anywhere in the code
        self.display_surface = pygame.display.get_surface()

        # read tileset and create group for every layer of the level
        self.border = self.create_tile_group(
            import_csv_layout(level_data.get("border")), "border"
        )

    @staticmethod
    def create_tile_group(layout: list, asset_type: str) -> pygame.sprite.Group:
        """
        Each csv file gives us a relative position for each tile
        x = col * tile size
        y = row * tile size

        :returns:
        A group of tile sprites with their coordinates and image loaded
        """
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":  # empty cell
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    sprites = import_sprites(
                        f"{TOP_LEVEL_DIR}/assets/tilesets/{asset_type}.png"
                    )
                    current_sprite = sprites[int(val)]
                    tile = Tile((x, y), current_sprite)
                    sprite_group.add(tile)
        return sprite_group

    def run(self):
        # update and draw
        self.border.draw(self.display_surface)
