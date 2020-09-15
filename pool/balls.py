import numpy as np
import pygame

from . import collisions


class Balls:
    """
    Class representing a collection of pool balls

    Might be slightly faster than an array of individual Ball objects (but we'll see....)

    """

    num_balls = 0
    positions = np.array([[]])
    velocities = np.array([[]])
    radii = np.array([])
    masses = np.array([])

    def __init__(self, num_balls):
        """
        Create some balls for testing

        """
        # TODO should track how many balls are moving and place stationary balls at the end of the list
        # Then we only need to check the first few balls for collisions
        # It might be inefficienct to move things around too much, but it might save a lot of time if only a few balls are moving
        self.num_balls = 2
        self.positions = np.array([[200, 350], [250, 350]])
        self.velocities = np.array([[1, 0], [-1, 0]])
        self.radii = np.random.randint(0, 10, size=self.num_balls)
        self.masses = np.square(self.radii)

    def draw(self, screen):
        """
        Draw these balls on a Pygame screen

        """
        for i in range(self.num_balls):
            pygame.draw.circle(
                screen, (255, 255, 255), self.positions[i].astype(int), self.radii[i]
            )

    def colliding(self, i: int, j: int) -> bool:
        """
        Detect whether particles i and j are colliding this timestep

        Quite naive, will miss a collision where particles step through each other

        TODO UT for this in the cases where they just touch, they intersect + they step past each other
        Also TODO UT for the case where they're touching but not moving

        """
        # Stationary balls don't collide
        if not np.any(self.velocities[i]) or not np.any(self.velocities[j]):
            return False

        return (self.positions[i][0] - self.positions[j][0]) ** 2 + (
            self.positions[i][1] - self.positions[j][1]
        ) ** 2 < (self.radii[i] + self.radii[j]) ** 2

    def resolve_collision(self, i: int, j: int) -> None:
        """
        Resolve a collision between particles i and j

        """
        # When balls collide, they bounce off each other
        v1_new, v2_new = collisions.non_relativistic_collision(
            self.velocities[i],
            self.velocities[j],
            self.positions[i],
            self.positions[j],
            self.masses[i],
            self.masses[j],
        )

        self.velocities[i] = v1_new
        self.velocities[j] = v2_new

    def move(self, x_limits, y_limits):
        """
        Move a collection of balls, processing collisions with the edges

        The wall limits are defined by two pairs (x_min, x_max) and (y_min, y_max)

        """
        # Move balls
        self.positions += self.velocities

        # Process collisions with the edges
        for i in range(self.num_balls):
            # Might not be quicker to do it all in one loop because of the cache
            # TODO make physically accurate
            if self.positions[i][0] < x_limits[0] or self.positions[i][0] > x_limits[1]:
                self.positions[i] -= 2 * self.velocities[i]
                self.velocities[i][0] *= -1
            if self.positions[i][1] < y_limits[0] or self.positions[i][1] > y_limits[1]:
                self.positions[i] -= 2 * self.velocities[i]
                self.velocities[i][1] *= -1

        # Very naive collision logic
        # Will miss the collisions between fast balls (they will step past each other)
        # Also is physically inaccurate
        # Also is inefficienct- checks every pair
        # TODO nicer
        for i in range(self.num_balls):
            for j in range(self.num_balls):
                if i != j:
                    if self.colliding(i, j):
                        self.resolve_collision(i, j)
