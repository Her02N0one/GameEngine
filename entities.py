import utils


class Player(utils.Entity):

    def __init__(self, x, y):
        super().__init__()
        self.set_position(x, y)
        self.set_texture("assets/sprites/test.png")
        self.scale(5)

    def move(self, dir_x, dir_y):
        self.set_position(self.sprite.x + dir_x, self.sprite.y + dir_y)

    def update_events(self, dt, event):
        pass

    def update(self, dt):
        pass

    def render(self, target, show_hitbox=False):

        target.blit(self.image, self.sprite)
