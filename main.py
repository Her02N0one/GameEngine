import pygame
import utils
from states import GameState

# gets window data from config file
with open("config/graphics.ini", "r") as f:
    line = f.read().splitlines()
    title = line[0]
    window_size = tuple(map(int, line[1].split()))
    fullscreen = int(line[2])
    fps = int(line[3])

if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(title)

running = True if pygame.display.get_surface() is not None else False

# set up clock for limiting framerate and getting dt
clock = pygame.time.Clock()
dt = 0.0

states = utils.Stack()  # Stack that holds all the States
state_data = dict(screen=screen, states=states)
states.push(GameState(state_data))


# ====== Main Game Loop ======

while running:
    clock.tick(fps)
    dt = clock.get_time()

    # Update
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if states.isEmpty() is not True:
        previous_state = states.top()
        states.top().update(dt)
        if previous_state != states.top():
            states.top().on_enter()
            previous_state.on_leave()
        if states.top().get_quit():
            states.top().end_state()
            states.pop()
    else:
        previous_state.on_leave()
        running = False

    # Render

    screen.fill((255, 255, 255))

    if not states.isEmpty():
        states.top().render()

    pygame.display.flip()


pygame.quit()
