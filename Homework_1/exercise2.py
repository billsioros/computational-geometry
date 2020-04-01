
from argparse import ArgumentParser
from math import cos, pi, sin

import matplotlib.pyplot as plt
import numpy as np


def lattice_points(radius):
    points = []

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x ** 2 + y ** 2 == radius ** 2:
                points.append((x, y))

    return points


if __name__ == "__main__":
    argparser = ArgumentParser(
        description="Lattice Points Visualizer"
    )

    argparser.add_argument(
        "-r", "--radius",
        type=int, required=True,
        help="The radius of the circle"
    )

    argparser.add_argument(
        "-s", "--sample",
        default=500,
        type=int, required=False,
        help="The number of points to be used when generating the circle"
    )

    argv = argparser.parse_args()

    phis = np.linspace(0, 2 * pi, argv.sample)

    cxs = [argv.radius * cos(phi) for phi in phis]
    cys = [argv.radius * sin(phi) for phi in phis]

    lattice_points = lattice_points(argv.radius)

    lxs = [point[0] for point in lattice_points]
    lys = [point[1] for point in lattice_points]

    plt.plot(cxs, cys, "k-")

    plt.plot(lxs, lys, 'b.', markersize=16)

    for point in lattice_points:
        x, y = point
        plt.text(x, y, '({}, {})'.format(x, y))

    plt.plot([0], [0], "kX", markersize=8)

    plt.title(
        f"The {len(lattice_points)} lattice points of a "
        f"circle of radius {argv.radius} "
        "with (0, 0) as center"
    )
    plt.grid()
    plt.xlim([-argv.radius, +argv.radius])
    plt.ylim([-argv.radius, +argv.radius])
    plt.axis('equal')
    plt.show()
