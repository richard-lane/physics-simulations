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

    def colliding(self, i: int, j: int) -> bool:
        """
        Detect whether particles i and j are colliding this timestep

        Quite naive, will miss a collision where particles step through each other

        TODO UT for this in the cases where they just touch, they intersect + they step past each other
        Also TODO UT for the case where they're touching but not moving

        """
        if (self.v_x[i] == 0 and self.v_y[i] == 0 and self.v_x[j] == 0  and self.v_y[j] == 0):
            return False

        return (self.x[i] - self.x[j]) ** 2 + (self.y[i] - self.y[j]) ** 2 < (
            self.r[i] + self.r[j]
        ) ** 2

    def resolve_collision(self, i: int, j: int) -> None:
        """
        Resolve a collision between particles i and j

        """
        # When balls collide, they stop
        print("ow")
        self.v_x[i], self.v_y[i] = 0, 0
        self.v_x[j], self.v_y[j] = 0, 0

    def move(self, x_limits, y_limits):
        """
        Move a collection of balls, processing collisions with the edges

        The wall limits are defined by two pairs (x_min, x_max) and (y_min, y_max)

        this should be a method idk why i moved it out

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

        # Very naive collision logic
        # Will miss the collisions between fast balls (they will step past each other)
        # Also is physically inaccurate
        # Also is inefficienct- checks every pair
        # TODO nicer
        for i in range(self.num_balls):
            # Check balls < i
            for j in range(i):
                if self.colliding(i, j):
                    self.resolve_collision(i, j)

            # Check balls > i
            for j in range(i + 1, self.num_balls):
                if self.colliding(i, j):
                    self.resolve_collision(i, j)
