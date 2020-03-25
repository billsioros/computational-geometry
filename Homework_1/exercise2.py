
import math


def lattice_points(radius):
    points = []

    for x in range(0, radius + 1):
        for y in range(0, radius + 1):
            if x ** 2 + y ** 2 == radius ** 2:
                points.append((x, y))

    return points


if __name__ == "__main__":
    print(lattice_points(100))
