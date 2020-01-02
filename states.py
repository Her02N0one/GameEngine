import dill
import pygame

import constants
import entities
import gui
import utils


class MainMenuState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/music/MainMenuSong.mp3")
        self.buttons = dict()
        self.buttons["NEW_GAME"] = gui.Button(y=10, text="New Game",
                                              callback=(lambda: self.states.push(GameState(state_data))))
        self.buttons["EDITOR"] = gui.Button(y=100, text="Editor",
                                            callback=(lambda: self.states.push(EditorState(state_data))))
        self.buttons["SETTINGS"] = gui.Button(y=190, text="Settings",
                                              callback=(lambda: self.states.push(SettingsState(state_data))))
        self.buttons["QUIT"] = gui.Button(y=430, text="Quit", callback=(lambda: self.end_state()))

    def on_enter(self):
        if bool(pygame.mixer.music.get_busy()) is not True:
            pygame.mixer.music.play(loops=-1)

    def on_leave(self):
        if self.buttons["SETTINGS"].is_pressed() is False:
            pygame.mixer.music.fadeout(900)

    def update_input(self, dt):
        pass

    def update_events(self, dt, event):

        for key in self.buttons:
            self.buttons[key].update_events(dt, event)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        # print(self.buttons["EDITOR"].is_pressed())
        for key in self.buttons:
            self.buttons[key].update(dt)

        # if keys[pygame.K_ESCAPE]:
        #     self.end_state()

    def render(self, target=None):

        if target is None:
            target = self.screen

        for key in self.buttons:
            self.buttons[key].render(target)


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        self.key_down = False
        self.player = entities.Player(32, 32)

    def on_enter(self):
        pass

    def on_leave(self):
        self.all_sprites.remove(self.player)
        self.entities.remove(self.player)

    def update_events(self, dt, event):
        # TODO: fix issue where when pressing multiple keys only the first key released responds
        if event.type == pygame.KEYDOWN:
            self.key_down = True
        elif event.type == pygame.KEYUP and self.key_down:
            if event.key == pygame.K_ESCAPE:
                self.end_state()
            self.key_down = False

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.player.jump(dt)
        if keys[pygame.K_a]:
            self.player.move(dt, dx=-1)
        if keys[pygame.K_d]:
            self.player.move(dt, dx=1)

        self.all_sprites.update(dt)

    def render(self, target=None):
        if target is None:
            target = self.screen

        for x in range(0, constants.WIDTH, constants.TILE_SIZE):
            pygame.draw.line(target, constants.GREY, (x, 0), (x, constants.HEIGHT))
        for y in range(0, constants.HEIGHT, constants.TILE_SIZE):
            pygame.draw.line(target, constants.GREY, (0, y), (constants.WIDTH, y))

        self.all_sprites.draw(target)


class SettingsState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        self.buttons = dict()

        self.buttons["BACK"] = gui.Button(y=430, text="Back", callback=(lambda: self.end_state()))
        self.slider = gui.Slider(initial_value=pygame.mixer.music.get_volume())

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

    def render(self, target=None):

        if target is None:
            target = self.screen

        for key in self.buttons:
            self.buttons[key].render(target)

        self.slider.render(target)


class EditorState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        self.selector = pygame.Rect((0, 0), (constants.TILE_SIZE, constants.TILE_SIZE))
        self.tile_map = [[0] * (constants.HEIGHT // constants.TILE_SIZE) for _ in
                         range((constants.WIDTH // constants.TILE_SIZE))]
        self.tile_pos = [0, 0]
        self.selected_tile = 0
        self.tile_color = constants.BLACK

    def update_events(self, dt, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.end_state()
            if event.key == pygame.K_1:
                self.tile_color = constants.BLACK
            if event.key == pygame.K_2:
                self.tile_color = constants.RED
            if event.key == pygame.K_3:
                self.tile_color = constants.GREEN
            if event.key == pygame.K_4:
                self.tile_color = constants.BLUE
            if event.key == pygame.K_5:
                self.tile_color = constants.LIGHT_RED
            if event.key == pygame.K_6:
                self.tile_color = constants.LIGHT_GREEN
            if event.key == pygame.K_7:
                self.tile_color = constants.LIGHT_YELLOW
            if event.key == pygame.K_8:
                self.tile_color = constants.GREY
            if event.key == pygame.K_c:
                self.tiles.empty()
            if event.key == pygame.K_s:
                with open("data", "wb") as f:
                    dill.load_types(unpickleable=True)
                    print(dill.detect.badobjects(self.selected_tile))
                    dill.dump(self.selected_tile, f)
                # self.tile_map = [[0] * (constants.HEIGHT // constants.TILE_SIZE) for _ in
                #                  range((constants.WIDTH // constants.TILE_SIZE))]

    def update(self, dt):

        self.tiles.update(dt)

        self.tile_pos = [pygame.mouse.get_pos()[0] // constants.TILE_SIZE,
                         pygame.mouse.get_pos()[1] // constants.TILE_SIZE]

        self.selector.x = self.tile_pos[0] * constants.TILE_SIZE
        self.selector.y = self.tile_pos[1] * constants.TILE_SIZE

        self.selected_tile = self.tile_map[self.tile_pos[0]][self.tile_pos[1]]

        if pygame.mouse.get_pressed()[0]:
            if self.selected_tile == 0 or self.selected_tile.color != self.tile_color:
                self.tiles.remove(self.selected_tile)
                # noinspection PyTypeChecker
                self.tile_map[self.tile_pos[0]][self.tile_pos[1]] = utils.Tile(col=self.tile_pos[0],
                                                                               row=self.tile_pos[1],
                                                                               color=self.tile_color)
        elif pygame.mouse.get_pressed()[2]:
            if self.selected_tile != 0:
                self.tiles.remove(self.selected_tile)
                self.tile_map[self.tile_pos[0]][self.tile_pos[1]] = 0

    def render(self, target=None):
        if target is None:
            target = self.screen

        for x in range(0, constants.WIDTH, constants.TILE_SIZE):
            pygame.draw.line(target, constants.GREY, (x, 0), (x, constants.HEIGHT))
        for y in range(0, constants.HEIGHT, constants.TILE_SIZE):
            pygame.draw.line(target, constants.GREY, (0, y), (constants.WIDTH, y))

        # for row in self.tile_map:
        #     for col in row:
        #         if col != 0:
        #             col.render(target)

        self.tiles.draw(target)

        pygame.draw.rect(target, (255, 0, 0), self.selector, 1)

        constants.small_font.render_to(target, (925, 0),
                                       f"({self.tile_pos[1]}, {self.tile_pos[0]})", (0, 0, 0))
