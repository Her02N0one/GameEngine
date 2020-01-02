import pygame

import constants


class StateStack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, state):
        if self.isEmpty() is not True:
            self.top().on_leave()
        self.items.append(state)
        self.top().on_enter()

    def pop(self):
        self.top().on_leave()
        self.items.pop()
        if self.isEmpty() is not True:
            self.top().on_enter()

    def top(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def __len__(self):
        return self.size()


class State:

    def __init__(self, state_data: dict):
        self.state_data = state_data
        self.screen = state_data["screen"]
        self.states = state_data["states"]

        self.all_sprites = constants.all_sprites
        self.entities = constants.entities
        self.tiles = constants.tiles

        self.mousePos = pygame.Vector2()
        self.quit = False
        self.target = None

    def get_quit(self):
        return self.quit

    def end_state(self):
        self.quit = True

    def on_enter(self):
        """
        Runs once every time the class enters top of the stack
        """
        pass

    def on_leave(self):
        """
        Runs once every time the class leaves top of the stack
        """
        pass

    def update_events(self, dt, event):
        assert 0, "update_input not implemented"

    def update_input(self, dt):
        assert 0, "update_input not implemented"

    def update(self, dt):
        assert 0, "update not implemented"

    def render(self, target=None):
        assert 0, "render not implemented"


class Tile(pygame.sprite.Sprite, object):

    def __init__(self, texture=None, row=0, col=0, width=constants.TILE_SIZE, height=constants.TILE_SIZE,
                 color=(0, 255, 0)):
        self.groups = constants.all_sprites, constants.tiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.color = color
        self.image.fill(color)
        self.y = self.rect.y = row * constants.TILE_SIZE
        self.x = self.rect.x = col * constants.TILE_SIZE
        # self.image = pygame.image.load(texture)

    def update(self, dt):
        pass

    def render(self, target):
        target.blit(self.image, self.rect)
