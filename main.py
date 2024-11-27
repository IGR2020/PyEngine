from tkinter.filedialog import askdirectory

from scene import Scene
from widgets import Button, Label


class EngineScene(Scene):
    def onInit(self):
        self.background = (30, 30, 30)
        self.projectPath = None
        while not self.projectPath:
            self.projectPath = askdirectory()
        self.tabs = [Label(0, 0, "Tab", "Scene", (255, 255, 255), 25, "Arialblack", stretchToFit=True, stretchBuffer=15)]

    def display(self) -> None:
        [tab.display(self.window) for tab in self.tabs]


if __name__ == "__main__":
    engineInstance = EngineScene((900, 500))
    engineInstance.start()