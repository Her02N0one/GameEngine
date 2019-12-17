import pygame

import utils


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def update_input(self, dt):
        pass

    def update(self, dt):
        self.update_mouse_positions()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_x]:
            self.states.push(TestState(self.state_data))

        if keys[pygame.K_v]:
            self.end_state()

    def render(self, target=None):

        if target is None:
            target = self.screen

        pygame.draw.rect(target, (255, 128, 128), pygame.Rect(30, 30, 200, 200))


class TestState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def update_input(self, dt):
        pass

    def update(self, dt):
        self.update_mouse_positions()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_c]:
            self.end_state()

    def render(self, target=None):

        if target is None:
            target = self.screen

        pygame.draw.rect(target, (255, 255, 0), pygame.Rect(30, 30, 200, 200))
