
from argparse import ArgumentParser
from random import uniform

import matplotlib.pyplot as plt
import numpy as np


def orientation(p1, p2, p3):
    return (p3[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


def counterclockwise(p1, p2, p3):
    return orientation(p1, p2, p3) > 0


def between(p1, p2, p3):
    if orientation(p1, p2, p3) != 0:
        return False

    if min(p1[0], p3[0]) > p2[0] or p2[0] > max(p1[0], p3[0]):
        return False

    if min(p1[1], p3[1]) > p2[1] or p2[1] > max(p1[1], p3[1]):
        return False

    return True


def jarvis(points):
    if len(points) < 3:
        return []

    points = sorted(points)

    convex_hull = [points[0]]

    current = None
    while True:
        current = points[0]
        for point in points[1:]:
            if current == convex_hull[-1] or \
                between(convex_hull[-1], current, point) or \
                    counterclockwise(convex_hull[-1], current, point):
                current = point

        if current == convex_hull[0]:
            break

        convex_hull.append(current)

    return convex_hull


if __name__ == "__main__":
    argparser = ArgumentParser(
        description=(
            "Visualizing the Convex Hull "
            "of a given set of points "
            "with the help of the Jarvis March Algorithm"
        )
    )

    argparser.add_argument(
        "-n", "--number",
        type=int, required=True,
        help="The number of points to be randomly generated"
    )

    argparser.add_argument(
        "-x", "--xrange",
        nargs='+', default=[-50, +50],
        type=int, required=False,
        help="The horizontal axis' range of values"
    )

    argparser.add_argument(
        "-y", "--yrange",
        nargs='+', default=[-50, +50],
        type=int, required=False,
        help="The vertical axis' range of values"
    )

    argv = argparser.parse_args()

    assert len(argv.xrange) == 2 and argv.xrange[0] < argv.xrange[1]
    assert len(argv.yrange) == 2 and argv.yrange[0] < argv.yrange[1]

    pxs = [uniform(argv.xrange[0], argv.xrange[1]) for _ in range(argv.number)]
    pys = [uniform(argv.yrange[0], argv.yrange[1]) for _ in range(argv.number)]

    points = [(x, y) for x, y in zip(pxs, pys)]

    convex_hull = jarvis(points)

    cxs = [point[0] for point in convex_hull]
    cys = [point[1] for point in convex_hull]

    plt.plot(pxs, pys, 'k.')
    plt.plot(cxs + [convex_hull[0][0]], cys + [convex_hull[0][1]], 'b-')

    plt.title(f"The Convex Hull of {argv.number} randomly generated points")
    plt.grid()
    plt.xlim([argv.xrange[0], argv.xrange[1]])
    plt.xlim([argv.yrange[0], argv.yrange[1]])
    plt.axis('equal')
    plt.show()
