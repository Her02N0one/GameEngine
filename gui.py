import pygame


class Button:
    def __init__(self,
                 x=10,
                 y=10,
                 width=200,
                 height=75,
                 text="Hello World",
                 idle_color=(100, 100, 100),
                 hover_color=(150, 150, 150),
                 active_color=(120, 120, 120),
                 callback=(lambda: None)
                 ):
        self.shape = pygame.Rect((x, y, width, height))
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.active_color = active_color
        self.current_color = idle_color
        self.font = pygame.font.SysFont("ariel", int(width / 4))
        self.textSurface = self.font.render(text, True, (200, 200, 200))
        self.textPos = (self.shape.x + (self.shape.width / 2) - self.font.size(text)[0] / 2,
                        self.shape.y + (self.shape.height / 2) - self.font.size(text)[1] / 2)

        self.button_down = False
        self.callback = callback

    def update_events(self, dt, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.shape.collidepoint(*event.pos):
                self.current_color = self.hover_color
                self.button_down = True

        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.shape.collidepoint(*event.pos) and self.button_down:
                self.callback()  # Call the function.
                self.current_color = self.active_color
            self.button_down = False

        elif event.type == pygame.MOUSEMOTION:
            collided = self.shape.collidepoint(*event.pos)
            if collided and not self.button_down:
                self.current_color = self.hover_color
            elif not collided:
                self.current_color = self.idle_color

    def render(self, target):
        pygame.draw.rect(target, self.current_color, self.shape)
        target.blit(self.textSurface, self.textPos)
