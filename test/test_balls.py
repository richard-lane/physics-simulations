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


def test_no_wall_bounce():
    """
    Check that a ball that isn't colliding with a wall is correctly identified

    """
    ball_system = balls.Balls(
        1, np.array([[20, 20]]), np.array([[10, 5]]), np.array([9])
    )

    assert ball_system.has_hit_wall(0, [0, 100], [0, 100]) is balls.WallBounce.NONE


def test_top_bottom_wall_intersection():
    """
    Check that a ball that intersecting with the top/bottom walls are detected

    """
    ball_system = balls.Balls(
        2,
        np.array([[50, 20], [50, 80]]),
        np.array([[0, 1], [0, 1]]),
        np.array([21, 21]),
    )

    assert ball_system.has_hit_wall(0, [0, 100], [0, 100]) is balls.WallBounce.Y
    assert ball_system.has_hit_wall(1, [0, 100], [0, 100]) is balls.WallBounce.Y


def test_left_right_wall_intersection():
    """
    Check that a ball that intersecting with the right/left walls are detected

    """
    ball_system = balls.Balls(
        2,
        np.array([[20, 50], [80, 50]]),
        np.array([[0, 1], [0, 1]]),
        np.array([21, 21]),
    )

    assert ball_system.has_hit_wall(0, [0, 100], [0, 100]) is balls.WallBounce.X
    assert ball_system.has_hit_wall(1, [0, 100], [0, 100]) is balls.WallBounce.X


def test_wall_bounce_touching():
    """
    Check a wall collision is detected when the ball is just touching it

    """
    ball_system = balls.Balls(
        1, np.array([[20, 30]]), np.array([[10, 5]]), np.array([20])
    )

    assert ball_system.has_hit_wall(0, [0, 100], [0, 100]) is balls.WallBounce.X


def test_corner_bounce():
    """
    Check a bounces with a corner where the ball intersects both walls, it intersects one and one touches, and it touches both

    """
    ball_system = balls.Balls(
        3,
        np.array([[19, 19], [19, 20], [20, 20]]),
        np.array([[1, 1], [1, 1], [1, 1]]),
        np.array([20, 20, 20]),
    )

    assert ball_system.has_hit_wall(0, [0, 100], [0, 100]) is balls.WallBounce.CORNER
    assert ball_system.has_hit_wall(1, [0, 100], [0, 100]) is balls.WallBounce.CORNER
    assert ball_system.has_hit_wall(2, [0, 100], [0, 100]) is balls.WallBounce.CORNER
