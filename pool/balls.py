import numpy as np
import pygame

from . import collisions


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
        self.x = np.random.randint(0, 500, size=num_balls)
        self.y = np.random.randint(0, 500, size=num_balls)
        self.v_x = np.random.randint(-10, 10, size=num_balls)
        self.v_y = np.random.randint(-10, 10, size=num_balls)
        self.r = np.random.randint(0, 10, size=num_balls)
        self.m = self.r

    def draw(self, screen):
        """
        Draw these balls on a Pygame screen

        """
        for i in range(self.num_balls):
            pygame.draw.circle(
                screen, (255, 255, 255), [self.x[i], self.y[i]], self.r[i]
            )


def move(balls_collection: Balls, x_limits, y_limits):
    """
    Move a collection of balls, processing collisions with the edges

    The wall limits are defined by two pairs (x_min, x_max) and (y_min, y_max)

    """
    # Move balls
    for i in range(balls_collection.num_balls):
        balls_collection.x[i] += balls_collection.v_x[i]
        balls_collection.y[i] += balls_collection.v_y[i]

    # Process collisions with the edges
    for i in range(balls_collection.num_balls):
        if balls_collection.x[i] < x_limits[0] or balls_collection.x[i] > x_limits[1]:
            balls_collection.x[i] -= 2 * balls_collection.v_x[i]
            balls_collection.v_x[i] *= -1

    # Might be quicker to do it all in one loop
    # but then again it might not, because of the cache
    for i in range(balls_collection.num_balls):
        if balls_collection.y[i] < y_limits[0] or balls_collection.y[i] > y_limits[1]:
            balls_collection.y[i] -= 2 * balls_collection.v_y[i]
            balls_collection.v_y[i] *= -1

    # Very naive collision logic
    # Will miss the collisions between fast balls (they will step past each other)
    # Also is physically inaccurate
    # Also is inefficienct- checks every pair
    # TODO nicer
    for i in range(balls_collection.num_balls):
        # Check balls < i
        for j in range(i):
            if (balls_collection.x[i] - balls_collection.x[j]) ** 2 + (balls_collection.y[i] - balls_collection.y[j]) ** 2 < (
                balls_collection.r[i] + balls_collection.r[j]
            ) ** 2:
                print("ow")

        # Check balls > i
        for j in range(i + 1, balls_collection.num_balls):
            if (balls_collection.x[i] - balls_collection.x[j]) ** 2 + (balls_collection.y[i] - balls_collection.y[j]) ** 2 < (
                balls_collection.r[i] + balls_collection.r[j]
            ) ** 2:
                print("ow")
