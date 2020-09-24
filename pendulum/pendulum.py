"""
Pendulum animation

"""
import numpy as np
from scipy.constants import g as EARTH_GRAVITY
from scipy.integrate import odeint


class Pendulum:
    """
    Class encapsulating the motion of a pendulum

    """

    _max_time = 0.0

    # Initial conditions as [initial_angular_vely, initial_angle]
    _initial_conditions = np.array([])

    # Angular freq in the harmonic limit, in rad/s
    _angular_freq = 0.0

    def __init__(
        self,
        length: np.float64,
        mass: np.float64,
        starting_angle: np.float64,
        starting_angular_vely: np.float64,
    ):
        """
        Initialise a pendulum with the given physical parameters and initial condition

        Starting angle and velocity in radians

        """

        # Initialise physical params
        # There's only one for a 1d pendulum
        self._angular_freq = np.sqrt(mass * EARTH_GRAVITY / length)

        # Initialise initial conditions
        self._initial_conditions = np.array([starting_angular_vely, starting_angle])

    def _eqns(self, x: np.ndarray, t):
        """
        Equation to be solved, in the form dx/dt  = something

        x is a vector of (dtheta/dt, theta)

        """
        # Could in principle sanity check the args but speed is probably paramount

        return np.array([-(self._angular_freq** 2) * np.sin(x[1]), x[0]])

    def solve(self, times: np.ndarray):
        """
        Solve the eqn of motion of the pendulum

        Returns [[velocities], [angles]]

        """
        # Should probably use solve_ivp instead
        return odeint(self._eqns, self._initial_conditions, times).T


def main():
    MyPendulum = Pendulum(1.0, 1.0, 1.0, 0.0)

    angles = MyPendulum.solve(np.arange(0, 10, 0.1))[1]

    print(angles)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
