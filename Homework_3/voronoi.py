
from random import seed, uniform

import click
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d


@click.command()
@click.option(
    '-s', '--seed',
    type=click.INT, default=None, show_default=True,
    help='the seed of the random number generator'
)
@click.option(
    '-n', '--number',
    type=click.INT, default=10, show_default=True,
    help='the number of random points to be generated'
)
@click.option(
    '-x', '--x-axis', 'x_axis',
    type=click.Tuple([float, float]), default=(-50.0, +50.0), show_default=True,
    help='the minimum and maximum horizontal coordinate value'
)
@click.option(
    '-y', '--y-axis', 'y_axis',
    type=click.Tuple([float, float]), default=(-50.0, +50.0), show_default=True,
    help='the minimum and maximum vertical coordinate value'
)
@click.option(
    '-f', '--filename',
    type=click.File('wb'),
    default=None,
    help='optionally save the figure in PNG format'
)
def cli(seed, number, x_axis, y_axis, filename):
    """Compute Voronoi diagrams of different sets of vertices"""

    if seed is not None:
        seed(seed)

    points = np.array([
        (
            uniform(x_axis[0], x_axis[1]),
            uniform(y_axis[0], y_axis[1])
        ) for _ in range(number)
    ])

    figure = voronoi_plot_2d(Voronoi(points))

    plt.title(f"The Voronoi Diagram of {len(points)} random points")

    if filename is None:
        plt.show()
    else:
        figure.savefig(filename, format="png")

if __name__ == '__main__':
    cli()
