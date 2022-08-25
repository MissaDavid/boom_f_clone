import os

TILE_SIZE = 64
NUM_TILES_IN_ROW = 17
NUM_TILES_IN_COL = 14
WIDTH = TILE_SIZE * NUM_TILES_IN_ROW
HEIGHT = TILE_SIZE * NUM_TILES_IN_COL
FPS = 60

TOP_LEVEL_DIR = os.path.join(os.getcwd())

LEVEL_ONE_DICT = {"border": f"{TOP_LEVEL_DIR}/assets/layouts/border.csv"}
