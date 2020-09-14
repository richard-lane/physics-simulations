"""
Library of functions for collisions

"""
import numpy as np
from . import balls


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


def non_relativistic_collision_collection(balls_collection, i: int, j: int):
    """
    Non relativistic collision between balls i and j in a collection of balls

    """
    v1_new, v2_new = non_relativistic_collision(
        (balls_collection.v_x[i], balls_collection.v_y[i]),
        (balls_collection.v_x[j], balls_collection.v_y[j]),
        (balls_collection.x[i], balls_collection.y[i]),
        (balls_collection.x[j], balls_collection.y[j]),
        balls_collection.m[i],
        balls_collection.m[j],
    )

    balls_collection.v_x[i], balls_collection.v_y[i] = v1_new
    balls_collection.v_x[j], balls_collection.v_y[j] = v2_new
