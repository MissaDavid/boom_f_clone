import os

from enum import Enum

TILE_SIZE = 32
NUM_TILES_IN_ROW = 17
NUM_TILES_IN_COL = 15
WIDTH = TILE_SIZE * NUM_TILES_IN_ROW
HEIGHT = TILE_SIZE * NUM_TILES_IN_COL
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 63, 229)

TOP_LEVEL_DIR = os.path.join(os.getcwd())
ASSET_FOLDER = f"{TOP_LEVEL_DIR}/assets"

TITLE_SCREEN_DICT = {"background": f"{ASSET_FOLDER}/layouts/title_screen.csv"}
LEVEL_ONE_DICT = {
    "border": f"{ASSET_FOLDER}/layouts/level_one_border.csv",
    "background": f"{ASSET_FOLDER}/layouts/level_one_background.csv",
    "breakables": f"{ASSET_FOLDER}/layouts/level_one_breakables.csv",
    "fixed": f"{ASSET_FOLDER}/layouts/level_one_fixed.csv",
    "player_one": f"{ASSET_FOLDER}/layouts/level_one_Player.csv",
}


class GameState(Enum):
    NEW_GAME = "New Game"
    QUIT = "Quit"
    TITLE = "Title Screen"
