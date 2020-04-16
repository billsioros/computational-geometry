import math

dimensions = range(1, 10, 2)

c = 2
e = 0.8

print("1-NN")
for dim in dimensions:
    frac = int(4 * c * math.sqrt(dim) / e)
    points = pow(frac, dim + 1)
    print(f"Dimension: {dim} points: {points}")

print("k-NN")
neighboors = range(2, 11, 1)
for k in neighboors:
    for dim in dimensions:
        frac = int((6 * c * math.sqrt(dim)) + k / e)
        points = pow(frac, dim + 1)
        print(f"k = {k} Dimension: {dim} points: {points}")

