
def counterclockwise(p1, p2, p3):
    return (p3[1] - p1[1]) * (p2[0] - p1[0]) > (p2[1] - p1[1]) * (p3[0] - p1[0])


def jarvis(points):
    if len(points) < 3:
        return []

    leftmost, convex_hull = sorted(points, key=lambda point: point[0])[0], []

    current = leftmost
    while not convex_hull or current != convex_hull[0]:
        convex_hull.append(current)

        current = points[0]
        for point in points[1:]:
            if current == convex_hull[-1] or counterclockwise(convex_hull[-1], current, point):
                current = point

    return convex_hull


if __name__ == "__main__":

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

    print(jarvis(points))
