import numpy as np
import pygame


class Balls:
    """
    Class representing a collection of pool balls

    Might be slightly faster than an array of individual Ball objects (but we'll see....)

    """

    x = np.array([])
    y = np.array([])
    v_x = np.array([])
    v_y = np.array([])
    r = np.array([])
    num_balls = 0

    def __init__(self, num_balls):
        """
        Create some randomly positioned, sized and directed balls

        """
        self.num_balls = num_balls
        self.x = np.random.randint(0, 100, size=num_balls)
        self.y = np.random.randint(0, 100, size=num_balls)
        self.v_x = np.random.randint(-10, 10, size=num_balls)
        self.v_y = np.random.randint(-10, 10, size=num_balls)
        self.r = np.random.randint(0, 10, size=num_balls)

    def move(self, x_limits, y_limits):
        """
        Move all the balls, processing collisions with the edges

        The wall limits are defined by two pairs (x_min, x_max) and (y_min, y_max)

        """
        # Move balls
        for i in range(self.num_balls):
            self.x[i] += self.v_x[i]
            self.y[i] += self.v_y[i]

        # Process collisions with the edges
        for i in range(self.num_balls):
            if self.x[i] < x_limits[0] or self.x[i] > x_limits[1]:
                self.x[i] -= 2 * self.v_x[i]
                self.v_x[i] *= -1

        # Might be quicker to do it all in one loop
        # but then again it might not, because of the cache
        for i in range(self.num_balls):
            if self.y[i] < y_limits[0] or self.y[i] > y_limits[1]:
                self.y[i] -= 2 * self.v_y[i]
                self.v_y[i] *= -1

    def draw(self, screen):
        """
        Draw these balls on a Pygame screen

        """
        for i in range(self.num_balls):
            pygame.draw.circle(
                screen, (255, 255, 255), [self.x[i], self.y[i]], self.r[i]
            )

