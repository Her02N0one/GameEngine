import pygame

import utils
from states import MainMenuState

# gets window data from config file
with open("config/graphics.ini", "r") as f:
    lines = f.read().splitlines()
    lines = list(map(lambda s: s.split("#")[0], lines))
    title = lines[0]
    window_size = tuple(map(int, lines[1].split()))
    fullscreen = int(lines[2])
    fps = int(lines[3])

if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(title)

running = True if pygame.display.get_surface() is not None else False
pygame.font.init()

# set up clock for limiting framerate and getting dt
clock = pygame.time.Clock()
dt = 0.0

states = utils.StateStack()  # Stack that holds all the States
state_data = dict(screen=screen, states=states)
states.push(MainMenuState(state_data))

# ====== Main Game Loop ======

while running:
    clock.tick(fps)
    dt = clock.get_time() / 1000


    # Update
    if states.isEmpty() is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            states.top().update_events(dt, event)

        states.top().update(dt)
        if states.top().get_quit():
            states.top().end_state()
            states.pop()
    else:
        running = False

    # Render

    screen.fill((255, 255, 255))

    if not states.isEmpty():
        states.top().render()

    pygame.display.flip()

pygame.quit()
