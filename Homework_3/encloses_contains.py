
import click
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.path import Path
from sympy import Circle, Point


@click.command()
@click.option(
    '-p', '--point',
    type=click.Tuple([float, float]),
    default=(2, 2), show_default=True,
    help='the target point'
)
@click.option(
    '-c', '--circle',
    type=click.Tuple([float, float, float]),
    default=(0, 0, 5), show_default=True,
    help='the circle\'s center and radius'
)
@click.option(
    '-s', '--sympy',
    type=click.Choice(['encloses_point', 'encloses']),
    default='encloses', show_default=True,
    help='the entity method'
)
@click.option(
    '-f', '--filename',
    type=click.File('wb'),
    default=None,
    help='optionally save the figure in PNG format'
)
def cli(point, circle, sympy, filename):
    """Comparing the `sympy.geometry` and `matplotlib.path` libraries"""

    figure = plt.figure()

    x, y = point
    plt.scatter([x], [y], c='r', marker='X')

    cx, cy, r = circle
    theta = np.linspace(0, 2 * np.pi, 500)
    plt.scatter([cx], [cy], c='b', marker='x')
    plt.plot(r * np.cos(theta) + cx, r * np.sin(theta) + cy, 'b--')

    plt.title(f'Comparing the .{sympy} and .contains_point methods')
    plt.grid()
    plt.xlim((-(r + 1) + cx, +(r + 1) + cx))
    plt.ylim((-(r + 1) + cy, +(r + 1) + cy))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()

    c1 = ['red', 'blue'][Path.circle((cx, cy), r).contains_point(point)]
    c2 = ['red', 'blue'][getattr(Circle((cx, cy), r), sympy)(Point(x, y))]

    p1 = mpatches.Patch(color=c1, label='.contains_point')
    p2 = mpatches.Patch(color=c2, label=f'.{sympy}')
    plt.legend(handles=[p1, p2], loc='upper left')


    if filename is None:
        plt.show()
    else:
        figure.savefig(filename, format="png")


if __name__ == '__main__':
    cli()
