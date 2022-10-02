import csv

import pygame

from game_settings import TILE_SIZE


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
    for sprite in obstacles:
        return rect.colliderect(sprite)
