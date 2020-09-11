import numpy as np


class Balls:
    """
    Class representing a collection of pool balls

    Might be slightly faster than an array of individual Ball objects (but we'll see....)

    """

    x = np.array()
    y = np.array()
    v_x = np.array()
    v_y = np.array()
    r = np.array()
    num_balls = 0

    def __init__(self, num_balls):
        self.num_balls = num_balls
        self.x = np.zeros(num_balls)
        self.y = np.zeros(num_balls)
        self.v_x = np.zeros(num_balls)
        self.v_y = np.zeros(num_balls)
        self.r = np.zeros(num_balls)

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
            if self.x[i] < x_limits[0] or self.x > x_limits[1]:
                self.x[i] -= 2 * self.v_x[i]

        # Might be quicker to do it all in one loop
        # but then again it might not, because of the cache
        for i in range(self.num_balls):
            if self.y[i] < y_limits[0] or self.y > y_limits[1]:
                self.y[i] -= 2 * self.v_y[i]

