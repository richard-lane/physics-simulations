"""
Testcases for collision logic

Hopefully wrong things should be obvious since we can see the balls collide

"""
import numpy as np
import pytest

from pool import collisions


def test_collision_wrong_dimension():
    """
    We can only deal with 2d things

    """
    two = (1, 2)
    three = (1, 2, 3)

    # Check mainline case
    # Weird list comprehension thing so that our particles aren't on top of each other when they collide
    collisions.non_relativistic_collision(two, two, [2 * x for x in two], two, 1, 1)

    # Error cases
    with pytest.raises(ValueError):
        collisions.non_relativistic_collision(three, two, two, two, 1, 1)
    with pytest.raises(ValueError):
        collisions.non_relativistic_collision(two, three, two, two, 1, 1)
    with pytest.raises(ValueError):
        collisions.non_relativistic_collision(two, two, three, two, 1, 1)
    with pytest.raises(ValueError):
        collisions.non_relativistic_collision(two, two, two, three, 1, 1)


def test_collision_stationary_target():
    """
    Test a collision with a stationary target

    """
    v1, v2 = (1, 0), (0, 0)
    x1, x2 = (0, 0), (1, 0)
    m1, m2 = 1, 1

    expected_v1_after = np.array([0, 0])
    expected_v2_after = np.array([1, 0])

    velocities_after = collisions.non_relativistic_collision(v1, v2, x1, x2, m1, m2)

    assert np.allclose(velocities_after[0], expected_v1_after)
    assert np.allclose(velocities_after[1], expected_v2_after)


def test_collision_moving_target():
    """
    Test a collision with a moving target

    """
    v1, v2 = (0, 2), (0, -4)
    x1, x2 = (0, 0), (0, 1)
    m1, m2 = 10, 2

    expected_v1_after = np.array([0, 0])
    expected_v2_after = np.array([0, 6])

    velocities_after = collisions.non_relativistic_collision(v1, v2, x1, x2, m1, m2)

    assert np.allclose(velocities_after[0], expected_v1_after)
    assert np.allclose(velocities_after[1], expected_v2_after)

