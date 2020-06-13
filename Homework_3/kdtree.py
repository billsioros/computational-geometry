
from re import sub

import click
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from knn import KNNForce, KNNTree
from options import Dictionary


@click.command()
@click.option(
    '-n', '--neighbors',
    default=1, show_default=True,
    help='the number of neighbors'
)
@click.option(
    '-t', '--train',
    type=click.Tuple([float, float]),
    default=[
        (0, 1), (2, 3), (4, 4),
        (2, 0), (5, 2), (6, 3)
    ], show_default=True,
    multiple=True,
    help='the training data'
)
@click.option(
    '-l', '--labels',
    type=click.INT,
    default=[0, 0, 0, 1, 1, 1], show_default=True,
    multiple=True,
    help='a list of labels, one for each training instance'
)
@click.option(
    '-m', '--mode',
    type=Dictionary({'force': KNNForce, 'tree': KNNTree}),
    default='force', show_default=True,
    help='brute force or kd-tree based k-neighborhood lookup'
)
@click.option(
    '-s', '--meshgrid-step', 'meshgrid_step',
    type=click.FLOAT,
    default=0.02, show_default=True,
    help=(
        'the meshgrid step determines the number of points, '
        'whose labels are going to be predicted by KNN, '
        'so that the underlying Voronoi diagram can be illustrated'
    )
)
@click.option(
    '-f', '--filename',
    type=click.File('wb'),
    default=None,
    help='optionally save the figure in PNG format'
)
def cli(neighbors, train, labels, mode, meshgrid_step, filename):
    """Perform various KD-Tree associated experiments"""

    cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#0000FF'])

    train, labels = np.array(train), np.array(labels)

    knn = mode(n_neighbors=neighbors)

    knn.fit(train, labels)

    x_min, x_max = train[:, 0].min() - 2, train[:, 0].max() + 2
    y_min, y_max = train[:, 1].min() - 2, train[:, 1].max() + 2

    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, meshgrid_step),
        np.arange(y_min, y_max, meshgrid_step)
    )

    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    figure = plt.figure()

    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    for x, y in zip(train[:, 0], train[:, 1]):
        dx = +0.1 if x > 0 else -0.1
        dy = +0.1 if y > 0 else -0.1
        plt.text(x + dx, y + dy, f'({x}, {y})', fontsize=10)

    plt.scatter(train[:, 0], train[:, 1], c=labels, cmap=cmap_bold)

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    plt.title(
        f'{neighbors}-NN Classification using the `{mode.__name__}`'
    )

    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()

    if filename is None:
        plt.show()
    else:
        figure.savefig(filename, format='png')


if __name__ == '__main__':
    cli()
