"""GUI for pygame (2.5.2 or beyond)"""

import pygame as pg
from pyautogui import mouseDown
from pygame.examples.sprite_texture import event

from assets import assets

mouseButtonMapping = {"left": 0, "middle": 1, "right": 2}

class BasicObject:
    def __init__(self, x: int, y: int, name: str):
        image = assets[name]
        self.rect = pg.Rect(x, y, image.get_width(), image.get_height())
        self.name = name

    def display(self, window: pg.Surface, x_offset: int, y_offset: int):
        window.blit(assets[self.name], (self.rect.x - x_offset, self.rect.y - y_offset))


class Button(BasicObject):
    def __init__(self, x: int, y: int, releasedImageName: str, pressedImageName: str, mouseButtonAccepted: str | int = None):
        """mouseButtonAccepted argument allows for you to check for only certain mouse button presses, possible arguments are 'left', 'right', 'middle', 0, 1, 2"""
        super().__init__(x, y, releasedImageName)

        self.releasedImageName = releasedImageName
        self.pressedImageName = pressedImageName

        self.heightDifference = assets[self.releasedImageName].get_height() - assets[self.pressedImageName].get_height()

        self.pressed = False
        if isinstance(mouseButtonAccepted, str): mouseButtonAccepted = mouseButtonMapping[mouseButtonAccepted]

        self.mouseButtonAccepted = mouseButtonAccepted


    def clicked(self, event, *args) -> bool:
        """Call within event loop under the if condition of pg.MOUSEBUTTONDOWN"""
        mousePos = pg.mouse.get_pos()

        if self.rect.collidepoint(mousePos) and (self.mouseButtonAccepted is None or event.button == self.mouseButtonAccepted):
            self.pressed = True
            self.name = self.pressedImageName
            self.rect.y += self.heightDifference
            return True

        return False

    def released(self, *args):
        """Call within event loop under the if condition of pg.MOUSEBUTTONUP"""
        if self.pressed:
            self.pressed = False
            self.name = self.releasedImageName
            self.rect.y -= self.heightDifference
            return True

        return False
