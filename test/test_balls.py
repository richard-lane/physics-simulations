import pytest
import numpy as np

from pool import balls


def test_balls_arg_verification():
    """
    Check we cant create a collection of balls with the wrong number/shape of positions, velocities or masses

    """
    two_pairs = np.array([[1, 2], [3, 4]])
    two_scalars = np.array([1, 2])

    # Mainline case
    balls.Balls(2, two_pairs, two_pairs, two_scalars)

    # Check error is raised when we have the wrong number of particles
    with pytest.raises(balls.ArgError):
        balls.Balls(3, two_pairs, two_pairs, two_scalars)

    # Check error is raised when we have the wrong numbers of positions
    with pytest.raises(balls.ArgError):
        balls.Balls(2, np.array([[1, 2], [2, 3], [3, 4]]), two_pairs, two_scalars)

    # Check error is raised when we have the wrong numbers of velocities
    with pytest.raises(balls.ArgError):
        balls.Balls(2, two_pairs, np.array([[1, 2], [3, 4], [4, 5]]), two_scalars)

    # Check error is raised when we have the wrong numbers of masses
    with pytest.raises(balls.ArgError):
        balls.Balls(2, two_pairs, two_pairs, np.array([1, 2, 3]))

    # Check error is raised when we have the wrong dimensionality
    with pytest.raises(balls.ArgError):
        balls.Balls(2, np.array([[1, 2, 3], [1, 2, 3]]), two_pairs, two_scalars)
    with pytest.raises(balls.ArgError):
        balls.Balls(2, two_pairs, np.array([[1, 2, 3], [1, 2, 3]]), two_scalars)
    with pytest.raises(balls.ArgError):
        balls.Balls(2, two_pairs, two_pairs, np.array([1, 2, 3]))


def test_ball_collision_overlap():
    """
    Check whether a simple collision where two balls overlap is detected

    """
    ball_system = balls.Balls(
        2, np.array([[0, 0], [10, 0]]), np.array([[5, 0], [0, 0]]), np.array([6, 6])
    )

    assert ball_system.colliding(0, 1)


def test_ball_collision_touching():
    """
    Check a simple collision where two balls just touch without overlapping

    """
    ball_system = balls.Balls(
        2, np.array([[0, 0], [10, 0]]), np.array([[5, 0], [0, 0]]), np.array([5, 5])
    )

    assert ball_system.colliding(0, 1)

def test_ball_no_collision():
    """
    Check two balls that aren't colliding are detected properly

    """
    ball_system = balls.Balls(
        2, np.array([[0, 0], [10, 0]]), np.array([[5, 0], [0, 0]]), np.array([3, 3])
    )

    assert not ball_system.colliding(0, 1)
