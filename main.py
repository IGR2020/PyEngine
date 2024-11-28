from scene import Scene
from widgets import Label, Hotbar

tabBarHeight = 55


class EngineScene(Scene):
    def onInit(self):
        self.background = (30, 30, 30)
        self.projectPath = "Place Holder"  # askdirectory()
        if len(self.projectPath) == 0:
            quit()
        self.tabs = Hotbar(0, 0, [
            Label(0, 0, "Unclicked Tab", "Scene", (255, 255, 255), 25, "Arialblack", "Clicked Tab", stretchToFit=True,
                  stretchBuffer=20,
                  data=Scene((self.width, self.height - tabBarHeight), "Untitled Scene", embedded=True))], "horizontal",
                           scrollMin=0, scrollMax=self.width)
        self.selectedTab = 0

    def display(self) -> None:
        self.tabs.objects[self.selectedTab].data.display()
        self.window.blit(self.tabs.objects[self.selectedTab].data.window, (0, tabBarHeight))
        for tab in self.tabs.objects:
            tab.display(self.window)

    def mouseDown(self, event):
        [tab.clicked(event) for tab in self.tabs.objects]

    def mouseUp(self, event):
        for i, tab in enumerate(self.tabs.objects):
            if tab.released(event):
                self.selectedTab = i

    def scroll(self, event):
        self.tabs.scroll(event, True)


if __name__ == "__main__":
    engineInstance = EngineScene((900, 500))
    engineInstance.start()
