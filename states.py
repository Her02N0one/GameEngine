import pygame

import gui
import utils


class MainMenuState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/music/MainMenuSong.mp3")
        self.buttons = dict()
        self.buttons["NEW_GAME"] = gui.Button(text="New Game",
                                              callback=(lambda: self.states.push(GameState(state_data))))
        self.buttons["TEST"] = gui.Button(y=230, text="Test Button")
        self.buttons["QUIT"] = gui.Button(y=430, text="Quit", callback=(lambda: self.end_state()))
        self.slider = gui.Slider()

    def on_enter(self):
        pygame.mixer.music.play(loops=-1)

    def on_leave(self):
        pygame.mixer.music.fadeout(1500)

    def update_input(self, dt):
        pass

    def update_events(self, dt, event):

        for key in self.buttons:
            self.buttons[key].update_events(dt, event)

        self.slider.update_events(dt, event)

    def update(self, dt):

        keys = pygame.key.get_pressed()

        for key in self.buttons:
            self.buttons[key].update(dt)

        self.slider.update(dt)
        pygame.mixer.music.set_volume(self.slider.get_percent())

        # if keys[pygame.K_ESCAPE]:
        #     self.end_state()

    def render(self, target=None):

        if target is None:
            target = self.screen

        for key in self.buttons:
            self.buttons[key].render(target)

        self.slider.render(target)


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        self.key_down = False

    def update_events(self, dt, event):
        # TODO: fix issue where when pressing multiple keys only the first key released responds
        if event.type == pygame.KEYDOWN:
            self.key_down = True
        elif event.type == pygame.KEYUP and self.key_down:
            if event.key == pygame.K_ESCAPE:
                self.end_state()
            if event.key == pygame.K_1:
                print("TEST")
            self.key_down = False

    def update(self, dt):
        pass

    def render(self, target=None):
        pass
