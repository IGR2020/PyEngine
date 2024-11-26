from scene import Scene
from widgets import Button


class EngineScene(Scene):
    def onInit(self):
        self.background = (30, 30, 30)
        self.tabs = [Button(0, 0, "Scene Tab", "Scene Tab")]

    def display(self) -> None:
        [tab.display(self.window) for tab in self.tabs]


if __name__ == "__main__":
    engineInstance = EngineScene((900, 500))
    engineInstance.start()