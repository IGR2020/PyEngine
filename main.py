from tkinter.filedialog import askdirectory

from scene import Scene
from widgets import Button, Label


class EngineScene(Scene):
    def onInit(self):
        self.background = (30, 30, 30)
        self.projectPath = askdirectory()
        if len(self.projectPath) == 0:
            quit()
        self.tabs = [
            Label(0, 0, "Unclicked Tab", "Scene", (255, 255, 255), 25, "Arialblack", "Clicked Tab", stretchToFit=True,
                  stretchBuffer=20)]

    def display(self) -> None:
        [tab.display(self.window) for tab in self.tabs]

    def mouseDown(self, event):
        [tab.clicked(event) for tab in self.tabs]

    def mouseUp(self, event):
        [tab.released(event) for tab in self.tabs]


if __name__ == "__main__":
    engineInstance = EngineScene((900, 500))
    engineInstance.start()
