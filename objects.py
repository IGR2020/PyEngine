import pygame as pg
from assets import *

class Package:
    def __init__(self) -> None:
        self.realPos = 0, 0
    
    def pack(self, window_width, window_height):
        self.realPos = self.rect.x / window_width, self.rect.y / window_height

    def unpack(self, window_width, window_height):
        x, y = self.realPos
        self.rect.topleft = x * window_width, y * window_height

class Button(Package):
    def __init__(self, pos, releasedImage, pressedImage, *args):
        # creating rect
        x, y = pos
        width, height = (
            assets[releasedImage].get_width(),
            assets[releasedImage].get_height(),
        )
        self.rect = pg.Rect(x, y, width, height)

        # setting pressed state
        self.releasedImage = releasedImage
        self.pressedImage = pressedImage

        # associated info
        if len(args) == 1:
            self.info = args[0]
        else:
            self.info = args

        # clicking
        self.is_pressed = False
        self.height_diffrence = (
            assets[self.releasedImage].get_height() - assets[self.pressedImage].get_height()
        )

        # packing
        self.realPos = 0, 0
        self.type = "Button"


    def clicked(self, pos=None, clicked_button: int = None) -> bool:
        if pos is None:
            pos = pg.mouse.get_pos()
        x, y = pos
        mouseDown = pg.mouse.get_pressed()
        if clicked_button is None:
            if True in mouseDown:
                mouseDown = True
            else:
                mouseDown = False
        else:
            mouseDown = mouseDown[clicked_button]

        if not self.is_pressed and mouseDown and self.rect.collidepoint((x, y)):
            self.rect.y += self.height_diffrence
            return True
        return False
    
    def pack(self, window_width, window_height):
        super().pack(window_width, window_height)

    def display(self, window, background=None):
        """
        background can be any RGB value
        """
        if background is not None:
            pg.draw.rect(window, background, self)
        if self.is_pressed:
            window.blit(assets[self.pressedImage], self)
        else:
            window.blit(assets[self.releasedImage], self)

    def pressed(self, pos=None, clicked_button: int = None) -> bool:
        if pos is None:
            pos = pg.mouse.get_pos()
        x, y = pos
        mouseDown = pg.mouse.get_pressed()
        if clicked_button is None:
            if True in mouseDown:
                mouseDown = True
            else:
                mouseDown = False
        else:
            mouseDown = mouseDown[clicked_button]
        if self.rect.collidepoint((x, y)) and mouseDown:
            self.is_pressed = True
        else:
            self.is_pressed = False
        return self.is_pressed

    def released(self, pos=None, clicked_button: int = None) -> bool:
        if pos is None:
            pos = pg.mouse.get_pos()
        x, y = pos
        mouseDown = pg.mouse.get_pressed()
        if clicked_button is None:
            if True in mouseDown:
                mouseDown = True
            else:
                mouseDown = False
        else:
            mouseDown = mouseDown[clicked_button]
        if not mouseDown and self.is_pressed:
            print("no?")
            self.rect.y -= self.height_diffrence
            return True
        if not self.rect.collidepoint((x, y)) and self.is_pressed:
            print("yes")
            self.rect.y -= self.height_diffrence
            return False
        return False

class Text(Package):
    def __init__(self, text, x, y, color, size, font,  center=False, centerx=False, centery=False) -> None:

        # saving reconstruction data
        super().__init__()
        self.text = text
        self.color = color
        self.size = size
        self.font = font

        # creating text surface
        font_style = pg.font.SysFont(self.font, self.size)
        text_surface = font_style.render(self.text, True, self.color)
        if center:
            x -= text_surface.get_width() // 2
            y -= text_surface.get_height() // 2
        else:
            if centerx:
                x -= text_surface.get_width() // 2
            if centery:
                y -= text_surface.get_height() // 2

        self.image = text_surface
        self.rect = text_surface.get_rect(topleft=(x, y))
        
        self.type = "Text"

    def pack(self, window_width, window_height):
        self.image = self.text
        return super().pack(window_width, window_height)
    
    def unpack(self, window_width, window_height):
        self.reload()
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        return super().unpack(window_width, window_height)
    
    def reload(self):
        font_style = pg.font.SysFont(self.font, self.size)
        text_surface = font_style.render(self.text, True, self.color)

        self.image = text_surface        

    def display(self, window):
        window.blit(self.image, self.rect)
