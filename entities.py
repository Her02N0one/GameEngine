import utils


class Player(utils.Entity):

    def __init__(self):
        super(Player, self).__init__()
        self.set_position()

    def update(self, dt, mouse_pos):
        pass

    def render(self, target, show_hitbox=False):
        pass
