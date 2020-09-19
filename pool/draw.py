import pygame
import numpy as np

from . import balls
from . import table


def draw():
    pygame.init()

    x_bounds = [0, 400]
    y_bounds = [0, 650]
    size = [x_bounds[1], y_bounds[1]]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Drawing test")
    done = False

    clock = pygame.time.Clock()

    # Create n balls with random positions on the screen and random velocities
    n = 10
    TestBalls = balls.Balls(
        n,
        np.random.randint(*x_bounds, size=(n, 2)).astype(np.float64),
        np.random.randint(-5, 5, size=(n, 2)).astype(np.float64),
        np.random.randint(4, 10, size=(n,)),
    )

    # Table border width
    border_width = 20
    internal_edges = [[border_width, size[0] - border_width], [border_width, size[1] - border_width]]

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Move balls
        TestBalls.move(internal_edges[0], internal_edges[1])

        # Draw background and balls
        table.draw_table(screen, *size, border_width)
        TestBalls.draw(screen)

        # Limit FPS
        clock.tick(60)

        # Update screen
        pygame.display.flip()

    pygame.quit()
