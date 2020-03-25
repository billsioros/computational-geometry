
import math

import numpy as np


def lattice_points(radius):
    points = []

    for x in range(0, radius + 1):
        for y in range(0, radius + 1):
            if x ** 2 + y ** 2 == radius ** 2:
                points.append((x, y))

    return points


print(lattice_points(1000))
