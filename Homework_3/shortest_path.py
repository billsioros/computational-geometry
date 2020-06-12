
from random import randrange, seed

import click
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path
from scipy.spatial import Delaunay

from decorators import safe
from options import Dictionary


def euclidean(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


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
    type=click.INT,
    default=50, show_default=True,
    help='the maximum horizontal coordinate value'
)
@click.option(
    '-y', '--y-axis', 'y_axis',
    type=click.INT,
    default=50, show_default=True,
    help='the maximum vertical coordinate value'
)
@click.option(
    '-m', '--metric',
    type=Dictionary({'euclidean': euclidean, 'manhattan': manhattan}),
    default='euclidean', show_default=True,
    help='the metric to be used when calculating the distance of two vertices'
)
@click.option(
    '-b', '--begin',
    type=click.INT,
    default=0, show_default=True,
    help='the starting vertex'
)
@click.option(
    '-e', '--end',
    type=click.INT,
    default=-1, show_default=True,
    help='the ending vertex'
)
@click.option(
    '-f', '--filename',
    type=click.File('wb'),
    default=None,
    help='optionally save the figure in PNG format'
)
@safe
def cli(seed, number, x_axis, y_axis, metric, begin, end, filename):
    """Compute the shortest path of different set of vertices in a tri-angulation"""

    if seed is not None:
        seed(seed)

    points = set()
    while len(points) != number:
        point = (randrange(0, x_axis), randrange(0, y_axis))
        if point not in points:
            points.add(point)

    points = sorted(points)
    indices = {point: i for i, point in enumerate(points)}
    points = np.array(points)

    tri = Delaunay(points)

    edges = np.ones((len(points), len(points))) * np.inf
    for triangle in points[tri.simplices]:
        for p1 in triangle:
            for p2 in triangle:
                tp1, tp2 = tuple(p1), tuple(p2)
                i, j = indices[tp1], indices[tp2]
                edges[i][j] = metric(tp1, tp2)

    dist_matrix, predecessors = shortest_path(
        csgraph=csr_matrix(edges),
        directed=False,
        return_predecessors=True
    )

    path = [end]

    predecessor = end
    while predecessors[begin, predecessor] > 0:
        path.append(predecessors[begin, predecessor])
        predecessor = predecessors[begin, predecessor]

    path.append(begin)

    xs = [points[i][0] for i in path[::-1]]
    ys = [points[i][1] for i in path[::-1]]

    figure = plt.figure()

    plt.plot(points[:, 0], points[:, 1], 'bo')

    for cx, cy in zip(points[:, 0], points[:, 1]):
        plt.text(
            cx - 0.5 if cx < 0 else cx + 0.5,
            cy - 0.5 if cy < 0 else cy + 0.5,
            f'({cx}, {cy})', fontsize=6
        )

    plt.triplot(points[:, 0], points[:, 1], tri.simplices, 'c-.')

    for i in range(len(path) - 1):
        plt.plot([xs[i], xs[i + 1]], [ys[i], ys[i + 1]], 'k-')

    plt.title(
        f'{dist_matrix[begin][end]:7.02f} units '
        f'from {tuple(points[begin])} to '
        f'{tuple(points[end])}'
    )

    if filename is None:
        plt.show()
    else:
        figure.savefig(filename, format="png")


if __name__ == '__main__':
    cli()
