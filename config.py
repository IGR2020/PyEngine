from objects import *


class BaseConfig:
    def __init__(self, obj, x, y) -> None:
        self.textBox = TextBox("Blank TextBox", "Blank TextBox Selected", 5, x, y, (220, 120, 120), 40, "ArialBlack", obj.name)
        self.obj = obj
        # flag for allowing objects like text to be changed and movment
        self.allowObjectModification = False
        self.allowObjectReposition = True

    def modify(self):
        # all GUI scripts
        self.textBox.select()

        self.obj.name = self.textBox.text

    def display(self, window):
        self.textBox.display(window)

    def event(self, event):
        self.textBox.update_text(event)

configMap = {}