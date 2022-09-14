import pygame

from game_settings import TILE_SIZE, ASSET_FOLDER
from player import Player
from tile import Tile
from utils import import_csv_layout, import_sprites


class Level:
    """
    Manages all sprites that are drawn on the display surface
    """

    def __init__(self, level_data: dict):
        # get display surface from anywhere in the code
        self.display_surface = pygame.display.get_surface()

        # read tileset and create group for every layer of the level

        # Static Tiles
        self.border = self.create_tile_group(
            import_csv_layout(level_data.get("border")), "border1"
        )
        self.background = self.create_tile_group(
            import_csv_layout(level_data.get("background")), "bg1"
        )
        self.fixed = self.create_tile_group(
            import_csv_layout(level_data.get("fixed")), "fixed"
        )

        # Interactive Tiles
        self.breakables = self.create_tile_group(
            import_csv_layout(level_data.get("breakables")), "breakable"
        )

        # Player
        self.player_one = self.create_tile_group(
            import_csv_layout(level_data.get("player_one")), "player_one"
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
        if asset_type == "player_one":
            sprite_group = pygame.sprite.GroupSingle()
        else:
            sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":  # empty cell
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if asset_type == "player_one":
                        tile = Player((x, y))
                    else:
                        sprites = import_sprites(
                            f"{ASSET_FOLDER}/tilesets/{asset_type}.png"
                        )
                        current_sprite = sprites[int(val)]
                        tile = Tile((x, y), current_sprite)

                    sprite_group.add(tile)

        return sprite_group

    def run(self):
        """
        Update and draw sprites
        """
        # static tiles
        self.border.draw(self.display_surface)
        self.background.draw(self.display_surface)
        self.fixed.draw(self.display_surface)

        # interactive tiles
        self.breakables.draw(self.display_surface)

        # player
        self.player_one.update()
        self.player_one.draw(self.display_surface)
