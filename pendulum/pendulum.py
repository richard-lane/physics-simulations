"""
Pendulum animation

"""
import numpy as np
from scipy.constants import g as EARTH_GRAVITY
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

        return np.array([-(self._angular_freq ** 2) * np.sin(x[1]), x[0]])

    def solve(self, times: np.ndarray):
        """
        Solve the eqn of motion of the pendulum

        Returns [[velocities], [angles]]

        """
        # Should probably use solve_ivp instead
        return odeint(self._eqns, self._initial_conditions, times).T


def animate(times: np.ndarray, angles: np.ndarray) -> None:
    """
    Plot a pendulum with the given angles at the given times

    Length is normalised to 1

    """
    x = np.sin(angles)
    y = -np.cos(angles)

    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
    ax.grid()

    line, = ax.plot([], [], "o-", lw=2)

    def init():
        line.set_data([], [])
        return (line,)

    def animate(i):
        thisx = [0, x[i]]
        thisy = [0, y[i]]

        line.set_data(thisx, thisy)
        return (line,)

    ani = animation.FuncAnimation(
        fig, animate, np.arange(1, len(y)), interval=25, blit=True, init_func=init
    )
    plt.show()


def main():
    MyPendulum = Pendulum(1.0, 1.0, 1.0, 0.0)

    times = np.arange(0.0, 100, 0.01)
    angles = MyPendulum.solve(times)[1]

    animate(times, angles)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
