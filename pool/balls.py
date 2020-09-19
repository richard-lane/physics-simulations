import numpy as np
import pygame
import enum

from . import collisions


class ArgError(Exception):
    """
    Invalid arguments passed to Balls constructor

    """

    pass


class WallBounce(enum.Enum):
    """
    Which wall a particle has bounced off

    Either no bounce, an X bounce (off left or right wall), a Y bounce (off top or bottom), a CORNER bounce or none

    In binary these are represented as (0, 1, 10, 11) which i guess enables bitwise comparisons

    """

    NONE = 0
    X = 1
    Y = 2
    CORNER = 3


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

    def __init__(
        self,
        num_balls: int,
        positions: np.ndarray,
        velocities: np.ndarray,
        radii: np.ndarray,
    ):
        """
        Create a collection of num_balls balls
        This could probably be inferred but i like having it explicit

        Positions and velocities should be an iterable of size (num_balls, 2) and should probably be floats

        Radii should be an iterable of ints, size (num_balls)

        """
        # Check that we have the right number of positions, velocities and radii
        if (
            len(positions) != num_balls
            or len(velocities) != num_balls
            or len(radii) != num_balls
        ):

            raise ArgError(
                f"{num_balls} balls; {len(positions)} positions; {len(velocities)} velocities and {len(radii)} radii"
            )

        # Check we have 2d positions and velocities, and scalar masses
        if (
            positions.shape != (num_balls, 2)
            or velocities.shape != (num_balls, 2)
            or radii.shape != (num_balls,)
        ):
            raise ArgError(
                f"Invalid dimensions: {positions.shape} positions; {velocities.shape} velocities; {radii.shape} radii"
            )

        # TODO should track how many balls are moving and place stationary balls at the end of the list
        # Then we only need to check the first few balls for collisions
        # It might be inefficienct to move things around too much, but it might save a lot of time if only a few balls are moving
        self.num_balls = num_balls
        self.positions = positions
        self.velocities = velocities
        self.radii = radii

        # All balls have mass proportional to their volume
        self.masses = self.radii ** 3

    def draw(self, screen: pygame.Surface):
        """
        Draw these balls on a Pygame screen

        """
        for i in range(self.num_balls):
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                np.ceil(self.positions[i]).astype(int),
                self.radii[i],
            )

    def has_hit_wall(self, i: int, x_limits, y_limits) -> bool:
        """
        Check whether particle i has collided with a wall

        Wall limits defined by x_limits, y_limits = [x_min, x_max], [y_min, y_max]

        """
        assert False

    def colliding(self, i: int, j: int) -> bool:
        """
        Detect whether particles i and j are colliding this timestep

        Quite naive, will miss a collision where particles step through each other

        TODO UT for this in the cases where they just touch, they intersect + they step past each other
        Also TODO UT for the case where they're touching but not moving

        """
        # Stationary balls don't collide
        # TODO i think this is breaking things when balls get stuck in each other
        if not np.any(self.velocities[i]) and not np.any(self.velocities[j]):
            return False

        return (self.positions[i][0] - self.positions[j][0]) ** 2 + (
            self.positions[i][1] - self.positions[j][1]
        ) ** 2 <= (self.radii[i] + self.radii[j]) ** 2

    def resolve_collision(self, i: int, j: int) -> None:
        """
        Resolve a collision between particles i and j

        """
        # TODO use move api
        # TODO move the right amount
        self.positions[i] -= 2 * self.velocities[i]
        self.positions[j] -= 2 * self.velocities[j]

        self.velocities[i], self.velocities[j] = collisions.non_relativistic_collision(
            self.velocities[i],
            self.velocities[j],
            self.positions[i],
            self.positions[j],
            self.masses[i],
            self.masses[j],
        )

    def wall_bounce(self, i: int, x_limits, y_limits) -> None:
        """
        Check whether particle i has hit a wall, and if so process the collision

        x_limits and y_limits should be two-element iterables

        """
        # Bouncing off a wall just reverses the relevant velocity

        # bounce off vertical wall
        if (
            self.positions[i][0] - self.radii[i] < x_limits[0]
            or self.positions[i][0] + self.radii[i] > x_limits[1]
        ):
            # Step back from the wall
            if self.positions[i][0] - self.radii[i] < x_limits[0]:
                # Left wall collision
                self.positions[i][0] += 2 * (
                    x_limits[0] + self.radii[i] - self.positions[i][0]
                )
            else:
                # Right wall collision
                self.positions[i][0] -= 2 * (
                    self.positions[i][0] + self.radii[i] - x_limits[1]
                )
            self.velocities[i][0] *= -1

        # Check both cases just in case we've hit the corner
        # bounce off horizontal wall
        if (
            self.positions[i][1] - self.radii[i] < y_limits[0]
            or self.positions[i][1] + self.radii[i] > y_limits[1]
        ):
            # Step back from the wall
            if self.positions[i][1] - self.radii[i] < y_limits[0]:
                # Top wall collision
                self.positions[i][1] += 2 * (
                    y_limits[0] + self.radii[i] - self.positions[i][1]
                )
            else:
                # Bottom wall collision
                self.positions[i][1] -= 2 * (
                    self.positions[i][1] + self.radii[i] - y_limits[1]
                )
            self.velocities[i][1] *= -1

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
            self.wall_bounce(i, x_limits, y_limits)

        # Very naive collision logic
        # Will miss the collisions between fast balls (they will step past each other)
        # Also is physically inaccurate
        # Also is inefficienct- checks every pair
        # TODO nicer
        # Maybe would be better to do these loops within the functions themselves
        for i in range(self.num_balls):
            for j in range(self.num_balls):
                if i != j:
                    if self.colliding(i, j):
                        self.resolve_collision(i, j)
