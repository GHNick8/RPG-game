class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.scenes = {}

    def add(self, name, scene):
        self.scenes[name] = scene

    def set(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)
