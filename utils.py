import csv

import pygame

from game_settings import TILE_SIZE, ASSET_FOLDER


def import_csv_layout(file) -> list:
    tileset_map = []
    with open(file) as f:
        csv_reader = csv.reader(f, delimiter=",")
        for row in csv_reader:
            tileset_map.append(row)

    return tileset_map


def import_sprites(file) -> list[pygame.Surface]:
    sprite_list = []
    spritesheet_surface = pygame.image.load(file).convert_alpha()
    x_num_tiles = int(spritesheet_surface.get_size()[0] / TILE_SIZE)
    y_num_tiles = int(spritesheet_surface.get_size()[1] / TILE_SIZE)

    for row in range(y_num_tiles):
        for col in range(x_num_tiles):
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            # create a new Surface to blit the sprite on it
            # with the SRCALPHA flag, the pixel format will include a per-pixel alpha
            # I use this so the target Surface becomes transparent
            sprite_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            new_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            new_surface.blit(spritesheet_surface, (0, 0), sprite_rect)

            sprite_list.append(new_surface)

    return sprite_list


def rect_has_collision(rect: pygame.Rect, obstacles: list[pygame.sprite.Group]) -> bool:
    """
    :param rect: a Rect
    :param obstacles: Group of sprites to check collisions with
    :return: bool True at the first collision found, else False
    """
    for sprite in obstacles:
        if rect.colliderect(sprite):
            return True

    return False


def create_tile_group_for_asset(
    layout_file: str, asset_name: str, sprite_cls, is_single_group: bool = False
) -> pygame.sprite.Group:
    """
    This util will import every sprite of a tileset and create a Group containing these sprites
    based on the desired class. It is possible to create a GroupSingle but this function will assume
    that you don't need to pass the current_sprite to the sprite_cls.

    Each csv file (layout file) gives us a relative position for each tile
        x = col * tile size
        y = row * tile size

    :param layout_file: the csv file name for a layout
    :param asset_name: the name of the file for that asset image
    :param sprite_cls: the sprite class that will make use of that asset
    :param is_single_group: boolean to know the type of group to create

    :return: A group of tile sprites with their coordinates and image loaded
    """
    layout = import_csv_layout(layout_file)
    group = pygame.sprite.GroupSingle() if is_single_group else pygame.sprite.Group()

    for row_index, row in enumerate(layout):
        for col_index, val in enumerate(row):
            if val != "-1":  # empty cell
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                sprites = import_sprites(f"{ASSET_FOLDER}/tilesets/{asset_name}.png")
                current_sprite = sprites[int(val)]

                if is_single_group:
                    group.add(sprite_cls((x, y)))
                else:
                    group.add(sprite_cls((x, y), current_sprite))

    return group
