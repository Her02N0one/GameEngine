import pygame
import pygame.freetype

pygame.freetype.init()
pygame.mixer.init()


class Button:
    # TODO: make a way to add different images for each button state

    def __init__(self,
                 x=10,
                 y=10,
                 width=200,
                 height=60,
                 text="",
                 font=pygame.freetype.SysFont(pygame.font.get_default_font(), 35),
                 idle_color=(100, 100, 100),
                 hover_color=(150, 150, 150),
                 active_color=(120, 120, 120),
                 hover_sound=pygame.mixer.Sound("assets/sounds/sfx/tap-resonant.aif"),
                 active_sound=pygame.mixer.Sound("assets/sounds/sfx/tap-warm.aif"),
                 callback=(lambda: None)
                 ):

        self.shape = pygame.Rect((x, y, width, height))
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.active_color = active_color
        self.hover_sound = hover_sound
        self.active_sound = active_sound
        self.text = text
        self.font = font
        self.textPos = ((self.shape.x + (self.shape.width / 2) - font.get_rect(text).width / 2),
                        (self.shape.y + (self.shape.height / 2) - font.get_rect(text).height / 2))

        self.current_color = idle_color
        self.button_down = False
        self.button_hover = False
        self.hover_sound_ready = True
        self.callback = callback

    def get_pressed(self) -> bool:
        return self.button_down

    def update_events(self, dt, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.shape.collidepoint(*event.pos):
                self.current_color = self.active_color
                self.active_sound.play()
                self.button_down = True

        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.shape.collidepoint(*event.pos) and self.button_down:
                self.callback()  # Call the function.
                self.current_color = self.hover_color
            self.button_down = False

        elif event.type == pygame.MOUSEMOTION:
            collided = self.shape.collidepoint(*event.pos)
            if collided and not self.button_down:
                self.current_color = self.hover_color
                if self.hover_sound_ready:
                    self.hover_sound.play()
                    self.hover_sound_ready = False
                self.button_hover = True
            elif self.button_hover and not collided:
                self.button_hover = False
                self.hover_sound_ready = True
            elif not collided:
                self.current_color = self.idle_color

    def update(self, dt):
        pass

    def render(self, target):
        pygame.draw.rect(target, self.current_color, self.shape)
        self.font.render_to(target, self.textPos, self.text, (0, 0, 0))


class Slider:
    # TODO: add a way for the slider to go up in increments based on a "ticks" variable
    def __init__(self,
                 x=200,
                 y=200,
                 width=200,
                 initial_value=0.5,
                 idle_slider_color=(120, 120, 120),
                 hover_slider_color=(100, 100, 100),
                 active_slider_color=(110, 110, 110),
                 line_color=(200, 200, 200),
                 active_line_color=(180, 180, 180),
                 progress_color=(180, 180, 255),
                 active_progress_color=(150, 150, 255),
                 ):

        self.radius = 8
        self.height = 5
        self.line = pygame.Rect((x, y), (width, self.height))
        self.slider = pygame.Rect((initial_value * self.line.width - (self.radius / 2) + self.line.x,
                                   y - (self.radius / 2) - self.line.height / 3),
                                  (self.radius * 2, self.radius * 2))

        self.progress = pygame.Rect((x, y), (self.slider.x - self.line.x, self.height))

        self.idle_slider_color = idle_slider_color
        self.hover_slider_color = hover_slider_color
        self.active_slider_color = active_slider_color
        self.line_color = line_color
        self.active_line_color = active_line_color
        self.progress_color = progress_color
        self.active_progress_color = active_progress_color

        self.current_slider_color = self.idle_slider_color
        self.current_line_color = self.line_color
        self.current_progress_color = self.progress_color

        self.button_down = False
        self.button_hover = False
        self.collided = False

    def get_percent(self):
        return (self.slider.x + self.radius / 2 - self.line.x) / self.line.width

    def update_events(self, dt, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider.collidepoint(*event.pos):
                self.current_slider_color = self.active_slider_color
                self.current_line_color = self.active_line_color
                self.current_progress_color = self.active_progress_color
                self.button_down = True
                self.collided = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.slider.collidepoint(*event.pos) and self.button_down:
                self.current_slider_color = self.hover_slider_color
                self.current_line_color = self.line_color
                self.current_progress_color = self.progress_color
            self.button_down = False
            self.collided = False

        elif event.type == pygame.MOUSEMOTION:
            if self.slider.collidepoint(*event.pos):
                self.current_slider_color = self.hover_slider_color
            if self.collided:
                self.slider.centerx = event.pos[0]
            elif not self.slider.collidepoint(*event.pos):
                self.current_slider_color = self.idle_slider_color
                self.current_progress_color = self.progress_color
                self.current_line_color = self.line_color

    def update(self, dt):
        if self.slider.x >= self.line.x + self.line.width - self.radius / 2:
            self.slider.x = self.line.x + self.line.width - self.radius / 2
        if self.slider.x <= self.line.x - self.radius / 2:
            self.slider.x = self.line.x - self.radius / 2
        self.progress.width = self.slider.x - self.line.x

    def render(self, target):

        pygame.draw.rect(target, self.current_line_color, self.line)
        pygame.draw.rect(target, self.current_progress_color, self.progress)
        pygame.draw.circle(target, self.current_slider_color, (self.slider.x + self.radius,
                                                               self.slider.y + self.radius), self.radius)
