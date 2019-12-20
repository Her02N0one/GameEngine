import pygame

import entities
import utils


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        self.player = entities.Player(100, 100)

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def update_input(self, dt):
        pass

    def update(self, dt):
        self.update_mouse_positions()

        keys = pygame.key.get_pressed()

        self.player.update(dt, self.mousePos)
        if keys[pygame.K_ESCAPE]:
            self.end_state()

    def render(self, target=None):

        if target is None:
            target = self.screen

        self.player.render(target)
