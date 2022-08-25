import sys

import pygame

from game_settings import WIDTH, HEIGHT, FPS, LEVEL_ONE_DICT
from level import Level
from logger import logger


class Game:
    def __init__(self):
        pygame.init()
        # calling display.set_mode() implicitly initializes pygame.display
        self.screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level(LEVEL_ONE_DICT)

    def run(self):
        pygame.display.set_caption("BOOM F")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    logger.info("Initialising game...")
    g = Game()
    logger.info("Initialised.")
    g.run()
