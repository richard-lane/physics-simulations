"""
Library of functions for collisions

"""
import numpy as np


def non_relativistic_collision(v1, v2, x1, x2, m1, m2):
    """
    Takes two iterables of Cartesian velocity vectors, two iterables of Cartesian position vectors and masses and returns two corresponding numpy arrays of their velocities after collision

    Only works with 2d velocities

    """
    if len(v1) != 2 or len(v2) != 2 or len(x1) != 2 or len(x2) != 2:
        raise ValueError("Only handles 2d velocities")

    # Some things that will be helpful for our calculation
    mass_sum = m1 + m2
    dv_dot_dx = (np.array(v1) - np.array(v2)).dot(np.array(x1) - np.array(x2))
    dx = np.array(x1) - np.array(x2)

    # I stole a formula from Wikipedia
    delta_v1 = (2 * m2 / mass_sum) * (dv_dot_dx / (dx.dot(dx))) * dx
    delta_v2 = -(2 * m1 / mass_sum) * (dv_dot_dx / (dx.dot(dx))) * dx

    return v1 - delta_v1, v2 - delta_v2
