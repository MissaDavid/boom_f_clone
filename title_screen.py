import pygame as py

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

    def draw(self):
        self.background.draw(self.display_surface)
