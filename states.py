import pygame
import utils
import entities


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

        print(self.mousePos)
        keys = pygame.key.get_pressed()

        self.player.update(dt, self.mousePos)

        if keys[pygame.K_v]:
            self.end_state()

    def render(self, target=None):

        if target is None:
            target = self.screen

        self.player.render(target)

        # pygame.draw.rect(target, (255, 128, 128), pygame.Rect(30, 30, 200, 200))
