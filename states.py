import pygame

import entities
import gui
import utils


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        self.player = entities.Player(100, 100)
        self.button = gui.Button()

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def update_input(self, dt):
        pass

    def update_events(self, dt, event):
        self.button.update_events(dt, event)
        self.player.update_events(dt, event)


    def update(self, dt):

        keys = pygame.key.get_pressed()

        self.player.update(dt)

        if keys[pygame.K_ESCAPE]:
            self.end_state()

    def render(self, target=None):

        if target is None:
            target = self.screen

        self.button.render(target)
        self.player.render(target)

        # pygame.draw.rect(target, (255, 128, 128), pygame.Rect(30, 30, 200, 200))
