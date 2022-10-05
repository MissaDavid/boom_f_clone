import sys

import pygame as py

from game_settings import (
    WIDTH,
    HEIGHT,
    LEVEL_ONE_DICT,
    WHITE,
    BLACK,
    BLUE,
    FPS,
    GameState,
    TITLE_SCREEN_DICT,
)
from level import Level
from logger import logger
from title_screen import TitleScreen
from ui_component import UIComponent


class Game:
    def __init__(self):
        py.init()
        # calling display.set_mode() implicitly initializes py.display
        self.screen = py.display.set_mode(size=(WIDTH, HEIGHT))
        self.clock = py.time.Clock()
        self.game_state = GameState.TITLE
        self.level = Level(LEVEL_ONE_DICT)
        self.title_screen = TitleScreen(TITLE_SCREEN_DICT)

    def show_title_screen(self):
        new_game_btn = UIComponent(
            position=(200, 240),
            font_size=int(26),
            text=GameState.NEW_GAME.value,
            text_rgb=WHITE,
            bg_rgb=BLUE,
            action=GameState.NEW_GAME,
        )
        quit_btn = UIComponent(
            position=(200, 350),
            font_size=int(26),
            text=GameState.QUIT.value,
            text_rgb=WHITE,
            bg_rgb=BLUE,
            action=GameState.QUIT,
        )

        while True:
            mouse_up = False
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type == py.MOUSEBUTTONUP:
                    mouse_up = True

            self.screen.fill(BLACK)
            self.title_screen.draw()

            for button in [new_game_btn, quit_btn]:
                if action := button.update(py.mouse.get_pos(), mouse_up):
                    return action

                button.draw(self.screen)

            py.display.update()
            self.clock.tick(FPS)

    def play(self, level):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()

            self.screen.fill(BLACK)
            level.run()

            py.display.update()
            self.clock.tick(FPS)

    def run(self):
        py.display.set_caption("BOOM F")

        while True:
            print(f"Running {self.game_state}")

            if self.game_state == GameState.TITLE:
                self.game_state = self.show_title_screen()

            if self.game_state == GameState.NEW_GAME:
                self.play(self.level)

            if self.game_state == GameState.QUIT:
                logger.info("Quitting game...")
                py.quit()
                sys.exit()


if __name__ == "__main__":
    logger.info("Initialising game...")
    g = Game()
    logger.info("Initialised. Running...")
    g.run()
