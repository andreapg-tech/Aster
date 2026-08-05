from render.eye import Eye

class Renderer:

    def __init__(self):
        self.left_eye = Eye(x = 250, y = 220, width = 80, height = 120)
        self.right_eye = Eye(x = 470, y = 220, width = 80, height = 120)

    def draw(self, surface):
        surface.fill((0, 0, 0)) #Clean the surface.
        self.left_eye.draw(surface)
        self.right_eye.draw(surface)