import pygame as py

from game_settings import ASSET_FOLDER, WIDTH, HEIGHT
from tile import Tile
from utils import create_tile_group_for_asset


class TitleScreen:
    """
    Title Screen with background sprites, a logo and a couple buttons
    """

    def __init__(self, layout: dict):
        self.display_surface = py.display.get_surface()

        self.background = create_tile_group_for_asset(
            layout.get("background"), "title_screen_bg", Tile
        )
        self.logo = py.image.load(f"{ASSET_FOLDER}/boom_logo.png").convert_alpha()
        self.logo_rect = self.logo.get_rect(center=(WIDTH / 2, HEIGHT / 3))

    def draw(self):
        self.background.draw(self.display_surface)
        self.display_surface.blit(self.logo, self.logo_rect)
