import pygame as py

from game_settings import ASSET_FOLDER, GameState

"""
This code was taken from the following tutorial on the blog _Programming Pixels_:
`https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html`
"""


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """Returns surface with text written on"""
    font = py.font.Font(f"{ASSET_FOLDER}/tempesta_seven.ttf", font_size)
    surface = font.render(text, False, text_rgb, bg_rgb)
    return surface.convert_alpha()


class UIComponent(py.sprite.Sprite):
    def __init__(
        self,
        position: tuple,
        text: str,
        font_size: int,
        bg_rgb: tuple,
        text_rgb: tuple,
        action: GameState = None,
    ):
        super().__init__()

        default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)
        highlighted_image = create_surface_with_text(
            text, int(font_size * 1.1), text_rgb, bg_rgb
        )
        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=position),
            highlighted_image.get_rect(center=position),
        ]
        self.mouse_over = False
        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up) -> GameState | None:
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            return self.action if mouse_up else None
        else:
            self.mouse_over = False
            return None

    def draw(self, surface) -> None:
        """Draws element onto a surface"""
        surface.blit(self.image, self.rect)
