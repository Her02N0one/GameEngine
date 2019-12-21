import pygame

import gui
import utils


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        self.button = gui.Button(text="New Game", callback=(lambda: print('starting new game')))

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def update_input(self, dt):
        pass

    def update_events(self, dt, event):
        self.button.update_events(dt, event)

    def update(self, dt):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.end_state()

    def render(self, target=None):

        if target is None:
            target = self.screen

        self.button.render(target)
