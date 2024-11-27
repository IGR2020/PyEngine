"""GUI for pygame (2.5.2 or beyond)"""

import pygame as pg

pg.font.init()
from assets import assets, fontLocation

mouseButtonMapping = {"left": 0, "middle": 1, "right": 2}


class BasicObject:
    def __init__(self, x: int, y: int, name: str):
        image = assets[name]
        self.rect = pg.Rect(x, y, image.get_width(), image.get_height())
        self.name = name

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0):
        window.blit(assets[self.name], (self.rect.x - x_offset, self.rect.y - y_offset))


class ObjectGroup:
    def __init__(self):
        self.objects = []
        self.rect = pg.Rect(1, 1, 1, 1)

    def setRect(self):
        for obj in self.objects:
            if obj.rect.x < self.rect.x:
                self.rect.x = obj.rect.x
            if obj.rect.y < self.rect.y:
                self.rect.y = obj.rect.y
            if obj.rect.right > self.rect.right:
                self.rect.right = obj.rect.right
            if obj.rect.bottom > self.rect.bottom:
                self.rect.bottom = obj.rect.bottom

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0):
        for obj in self.objects:
            obj.display(window, x_offset, y_offset)


class Button(BasicObject):
    def __init__(self, x: int, y: int, releasedImageName: str, pressedImageName: str,
                 mouseButtonAccepted: str | int = None, data=None):
        """mouseButtonAccepted argument allows for you to check for only certain mouse button presses, possible arguments are 'left', 'right', 'middle', 0, 1, 2
        \nPlace any associated data of the button as the data argument"""
        super().__init__(x, y, releasedImageName)

        self.releasedImageName = releasedImageName
        self.pressedImageName = pressedImageName

        self.heightDifference = assets[self.releasedImageName].get_height() - assets[self.pressedImageName].get_height()

        self.pressed = False
        if isinstance(mouseButtonAccepted, str): mouseButtonAccepted = mouseButtonMapping[mouseButtonAccepted]

        self.mouseButtonAccepted = mouseButtonAccepted

        self.data = data

    def clicked(self, event, *args) -> bool:
        """Call within event loop under the if condition of pg.MOUSEBUTTONDOWN"""
        mousePos = pg.mouse.get_pos()

        if self.rect.collidepoint(mousePos) and (
                self.mouseButtonAccepted is None or event.button == self.mouseButtonAccepted):
            self.pressed = True
            self.name = self.pressedImageName
            self.rect.y += self.heightDifference
            return True

        self.pressed = False
        return False

    def released(self, *args):
        """Call within event loop under the if condition of pg.MOUSEBUTTONUP"""
        if self.pressed:
            self.pressed = False
            self.name = self.releasedImageName
            self.rect.y -= self.heightDifference
            return True

        return False

    def reload(self):
        super().__init__(self.rect.x, self.rect.y, self.releasedImageName)

        self.releasedImageName = self.releasedImageName
        self.pressedImageName = self.pressedImageName

        self.heightDifference = assets[self.releasedImageName].get_height() - assets[self.pressedImageName].get_height()


class Text:
    def __init__(self, text, x, y, color, size, font, center=False) -> None:

        # saving reconstruction data
        self.text = str(text)
        self.color = color
        self.size = size
        self.font = font

        # creating text surface
        font_style = pg.font.Font(fontLocation + self.font + ".ttf", self.size)
        text_surface = font_style.render(self.text, True, self.color)
        if center:
            x -= text_surface.get_width() // 2
            y -= text_surface.get_height() // 2

        self.image = text_surface
        self.rect = text_surface.get_rect(topleft=(x, y))

        self.type = "Text"

    def reload(self, reloadRect=True):
        font_style = pg.font.Font(fontLocation + self.font + ".ttf", self.size)
        text_surface = font_style.render(self.text, True, self.color)

        self.image = text_surface

        if reloadRect:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y - y_offset))


class Label(ObjectGroup, Button):
    def __init__(self, x: int, y, labelName, text, color: tuple[int, int, int], size, font,
                 clickedLabelName: str = None, stretchToFit=False, stretchBuffer=0, data=None):
        if clickedLabelName is None: clickedLabelName = labelName

        ObjectGroup.__init__(self)
        Button.__init__(self, x, y, labelName, clickedLabelName, data=data)
        self.objects.append(
            Text(text, self.rect.centerx, self.rect.centery, color, size, font, center=True)
        )

        if stretchToFit:
            assets[f"Stretched {labelName}"] = pg.transform.scale(assets[labelName], (
            self.objects[0].rect.width + stretchBuffer, self.objects[0].rect.height + stretchBuffer))

            assets[f"Stretched {clickedLabelName}"] = pg.transform.scale(assets[clickedLabelName], (
            self.objects[0].rect.width + stretchBuffer, self.objects[0].rect.height + stretchBuffer - self.heightDifference))

            self.releasedImageName = f"Stretched {labelName}"
            self.pressedImageName = f"Stretched {clickedLabelName}"

            Button.reload(self)

        self.objects[0].rect.center = self.rect.center

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0):
        Button.display(self, window, x_offset, y_offset)
        ObjectGroup.display(self, window, x_offset, y_offset)

    def clicked(self, event, *args) -> bool:
        val = Button.clicked(self, event, *args)
        if val:
            self.objects[0].rect.y += self.heightDifference
        return val

    def released(self, *args):
        val = Button.released(self, *args)
        if val:
            self.objects[0].rect.y -= self.heightDifference
        return val