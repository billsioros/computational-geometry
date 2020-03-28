
def counterclockwise(p1, p2, p3):
    return (p3[1] - p1[1]) * (p2[0] - p1[0]) > (p2[1] - p1[1]) * (p3[0] - p1[0])


def between(p1, p2, p3):
    if (p2[1] - p1[1]) * (p3[0] - p1[0]) != (p3[1] - p1[1]) * (p2[0] - p1[0]):
        return False

    if min(p1[0], p3[0]) >= p2[0] or p2[0] >= max(p1[0], p3[0]):
        return False

    if min(p1[1], p3[1]) >= p2[1] or p2[1] >= max(p1[1], p3[1]):
        return False

    return True


def jarvis(points):
    if len(points) < 3:
        return []

    points = sorted(points)

    convex_hull = [points[0]]

    current = None
    while current != convex_hull[0]:
        current = points[0]
        for point in points[1:]:
            if current == convex_hull[-1] or \
                between(convex_hull[-1], point, current) or \
                    counterclockwise(convex_hull[-1], current, point):
                current = point

        convex_hull.append(current)

    return convex_hull


if __name__ == "__main__":

    from random import sample

    points = [
        (-1.1864675231268604, 0.8604977064876449),
        (0.254077253342894, 0.4165505096669816),
        (1.1850673584446412, 0.9339467765661142),
        (-0.6735263325201089, 0.21170624429821794),
        (-0.14850235634414555, 0.0669557287369027),
        (0.5409696919027351, -0.3930113284638238),
        (-1.4293971972661237, -1.4296433458005595),
        (0.02954097653197485, -0.4244467627683465),
        (1.242789451246841, 0.7853986196799201)
    ]

    points = [
        (-1, +1), (+0, +1), (+1, +1),
        (-1, +0), (+0, +0), (+1, +0),
        (-1, -1), (+0, -1), (+1, -1)
    ]

    print(jarvis(sample(points, len(points))))
