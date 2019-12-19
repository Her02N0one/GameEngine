import pygame


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

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

        self.mousePos = pygame.Vector2()
        self.quit = False
        self.target = None

    def get_quit(self):
        return self.quit

    def end_state(self):
        self.quit = True

    def update_mouse_positions(self):
        self.mousePos.update(pygame.mouse.get_pos())

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

    def update_input(self, dt):
        assert 0, "update_input not implemented"

    def update(self, dt):
        assert 0, "update not implemented"

    def render(self, target=None):
        assert 0, "render not implemented"


class Entity:

    def __init__(self):
        self.sprite = pygame.Rect(0, 0, 0, 0)
        self.image = pygame.Surface((0, 0))
        # self.movementComponent = None

    def set_texture(self, texture):
        self.image = pygame.image.load(texture)

    def set_position(self, x, y):
        self.sprite.x = x
        self.sprite.y = y

    def set_size(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.sprite.width = width
        self.sprite.height = height

    # TODO: fix my movement component
    # def move(self, dir_x, dir_y, dt):
    #     if self.movementComponent is not None:
    #         self.movementComponent.move(dir_x, dir_y, dt)

    def update(self, dt, mouse_pos):
        assert 0, "update not implemented"

    def render(self, target, show_hitbox=False):
        assert 0, "render not implemented"
