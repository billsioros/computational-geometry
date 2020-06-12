
from random import seed, uniform

import click
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
import os

@click.command()
@click.option(
    '-s', '--seed',
    type=click.INT,
    default=None, show_default=True,
    help='the seed of the random number generator'
)
@click.option(
    '-n', '--number',
    type=click.INT,
    default=10, show_default=True,
    help='the number of random points to be generated'
)
@click.option(
    '-x', '--x-axis', 'x_axis',
    type=click.Tuple([float, float]),
    default=(-50.0, +50.0), show_default=True,
    help='the minimum and maximum horizontal coordinate value'
)
@click.option(
    '-y', '--y-axis', 'y_axis',
    type=click.Tuple([float, float]),
    default=(-50.0, +50.0), show_default=True,
    help='the minimum and maximum vertical coordinate value'
)
@click.option(
    '-f', '--filename',
    type=click.File('wb'),
    default=None,
    help='optionally save the figure in PNG format'
)
def cli(seed, number, x_axis, y_axis, filename):
    """Compute the Delaunay triangulation of different sets of vertices"""

    if seed is not None:
        seed(seed)

    points = np.array([
        (
            uniform(x_axis[0], x_axis[1]),
            uniform(y_axis[0], y_axis[1])
        ) for _ in range(number)
    ])

    figure = plt.figure()

    plt.triplot(points[:,0], points[:,1], Delaunay(points).simplices)
    plt.plot(points[:,0], points[:,1], 'o')
    plt.title(f"The Delaunay triangulation of {len(points)} random points")

    if filename is None:
        plt.show()
    else:
        figure.savefig(filename, format="png")

if __name__ == '__main__':
    cli()
