
# Computational Geometry - Homework 1

---

## Contributors

* [Sioros Vasileios (1115201500144)](https://github.com/billsioros)
* [Andrinopoulou Christina (1115201500006)](https://github.com/ChristinaAndrinopoyloy)

---

## Exercises

### Exercise No.1

#### Introduction

<!-- TODO -->

#### Instructions

<!-- TODO -->

---

### Exercise No.2

#### Introduction

In an x–y Cartesian coordinate system, the circle with centre coordinates (a, b) and radius r is the set of all points (x, y) such that

```python
(x - a) ** 2 + (y - b) ** 2 == r ** 2
```

If the circle is centred at the origin (0, 0), then the equation simplifies to

```python
x ** 2 + y ** 2 == r ** 2
```

The lattice points on the circumference of a circle, are the points along the circumference that have integer coordinates.

Any point whose euclidean distance to the center of the circle is greater than the radius of the circle does not belong to the circle.

Thus, if the circle is centred at the origin `(0, 0)`, any point whose x or y coordinate' s absolute value is greater than the radius of the circle does not belong to the circle.

Hence, the lattice points are a subset of the set of points which have as x and y coordinates, integer values in the range `[-radius, +radius]`.

For example, for a circle with a radius of 1 we only need to check the points

```python
[(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
```

```python
def lattice_points(radius):
    points = []

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x ** 2 + y ** 2 == radius ** 2:
                points.append((x, y))

    return points
```

#### Instructions

```txt
$ python -m virtualenv .env
$ source .env/Scripts/activate
$ pip install -r requirements.txt
$ python exercise2.py -h
usage: exercise2.py [-h] -r RADIUS [-s SAMPLE]

Lattice Points Visualizer

optional arguments:
  -h, --help            show this help message and exit
  -r RADIUS, --radius RADIUS
                        The radius of the circle
  -s SAMPLE, --sample SAMPLE
                        The number of points to be used when generating the
                        circle
$ python exercise2.py -r 5
```

### Exercise No.3

#### Introduction

<!-- TODO -->

#### Instructions

<!-- TODO -->

---

### Exercise No.4

#### Introduction

<!-- TODO -->

```python
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
```

#### Instructions

```txt
$ python -m virtualenv .env
$ source .env/Scripts/activate
$ pip install -r requirements.txt
$ python exercise4.py -h
usage: exercise4.py [-h] -n NUMBER [-x XRANGE [XRANGE ...]]
                    [-y YRANGE [YRANGE ...]]

Visualizing the Convex Hull of a given set of points with the help of the
Jarvis March Algorithm

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        The number of points to be randomly generated
  -x XRANGE [XRANGE ...], --xrange XRANGE [XRANGE ...]
                        The horizontal axis' range of values
  -y YRANGE [YRANGE ...], --yrange YRANGE [YRANGE ...]
                        The vertical axis' range of values
$ python exercise4.py -n 20
```
