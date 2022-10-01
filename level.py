import pygame

from bomb import Dispersion, Bomb
from game_settings import TILE_SIZE, ASSET_FOLDER
from player import Player
from tile import Interactive, Tile
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
        self.bomb_group = pygame.sprite.Group()
        self.bomb_dispersion_group = pygame.sprite.Group()

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

                    sprites = import_sprites(
                        f"{ASSET_FOLDER}/tilesets/{asset_type}.png"
                    )
                    current_sprite = sprites[int(val)]

                    if asset_type == "player_one":
                        sprite_group.add(Player((x, y)))
                    elif asset_type == "breakable":
                        sprite_group.add(Interactive((x, y), current_sprite))
                    else:
                        sprite_group.add(Tile((x, y), current_sprite))

        return sprite_group

    def set_bomb_dispersion(self, bomb) -> None:
        up = Dispersion((bomb.rect.x, bomb.rect.y - TILE_SIZE))
        down = Dispersion((bomb.rect.x, bomb.rect.y + TILE_SIZE))
        left = Dispersion((bomb.rect.x - TILE_SIZE, bomb.rect.y))
        right = Dispersion((bomb.rect.x + TILE_SIZE, bomb.rect.y))
        self.bomb_dispersion_group.add([up, down, left, right])

    def can_set_bomb(self, x, y) -> bool:
        rect = pygame.Rect((x, y), (TILE_SIZE, TILE_SIZE))
        for sprite in self.bomb_group.sprites():
            if rect.colliderect(sprite):
                return False

        return True

    def explode_breakables(self):
        collisions = []
        for hitbox in self.bomb_dispersion_group.sprites():
            breakable = pygame.sprite.spritecollideany(hitbox, self.breakables)
            if breakable:
                collisions.append(breakable)

        for block in collisions:
            print(len(collisions))
            block.update()

    def run(self):
        """
        Update and draw sprites
        """
        # static tiles drawing
        self.border.draw(self.display_surface)
        self.background.draw(self.display_surface)
        self.fixed.draw(self.display_surface)

        # interactive tiles drawing
        self.breakables.draw(self.display_surface)

        # Player drawing and update
        all_obstacles = (
            self.border.sprites() + self.fixed.sprites() + self.breakables.sprites()
        )
        self.player_one.update(all_obstacles)
        self.player_one.draw(self.display_surface)

        # Bomb drawing and update
        p = self.player_one.sprites()[0]
        if p.has_triggered_bomb:
            p.has_triggered_bomb = False
            if self.can_set_bomb(p.rect.x, p.rect.y):
                b = Bomb((p.rect.x, p.rect.y))
                self.bomb_group.add(b)
                self.set_bomb_dispersion(b)

        self.bomb_group.draw(self.display_surface)
        self.bomb_group.update()
        self.explode_breakables()
