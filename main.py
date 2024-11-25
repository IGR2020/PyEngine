from scene import Scene


class EngineScene(Scene):
    def onInit(self):
        self.background = (30, 30, 30)
        self.tabs = []

if __name__ == "__main__":
    engineInstance = EngineScene((900, 500))
    engineInstance.start()