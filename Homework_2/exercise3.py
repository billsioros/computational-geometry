
from math import atan2, degrees, sqrt
from os import makedirs, path
from re import sub

import click
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier


def euclidean(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


@click.command()
@click.option("--neighbors", default=1, help="the number of neighbors to use")
@click.option("--metric", default="minkowski", help="the distance metric to use")
@click.option("--p", default=2, help="power parameter for the Minkowski metric")
@click.option("--step", default=0.02, help="The step size in the mesh")
@click.option("--offset", default=0.1, help="the coordinate label offset")
@click.option("--margin", default=2, help="the x, y axis margin")
@click.option(
    "--fit",
    type=click.Tuple([float, float]),
    default=[
        (0, 1), (2, 3), (4, 4),
        (2, 0), (5, 2), (6, 3)
    ],
    multiple=True,
    help="fit the model using 'fit' as training data and 'classes' as target values"
)
@click.option(
    "--classes",
    type=int,
    default=[0, 0, 0, 1, 1, 1],
    multiple=True,
    help="fit the model using 'fit' as training data and 'classes' as target values"
)
@click.option(
    "--predict",
    type=click.Tuple([float, float]),
    default=None,
    multiple=True,
    help="predict the class labels for the provided data."
)
@click.option("--connect", is_flag=True, help="show connecting line to k nearest neighbors")
@click.option("--save", is_flag=True, help="save the resulting figure")
@click.option("--filename", default=None, help="where to save the resulting figure")
def classify(
    neighbors, metric, p,
    step, offset, margin,
    fit, classes, predict, connect,
    save, filename
):
    """
    Demonstrate the differences in decision boundaries
    in regards to K-NN classification
    """

    fit = list(dict.fromkeys(fit))
    fit = np.array([np.array(x) for x in fit])
    classes = np.array(classes)

    # Create color maps
    cmap_light = ListedColormap(["#FFAAAA", "#AAAAFF"])
    cmap_bold = ListedColormap(["#FF0000", "#0000FF"])

    title = f"{neighbors}-NN Classification using the {metric} ({p}) metric"

    # We create an instance of Neighbours Classifier and fit the data.
    knn = KNeighborsClassifier(
        neighbors,
        weights="uniform",
        metric=metric,
        p=p
    )
    knn.fit(fit, classes)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = fit[:, 0].min() - margin, fit[:, 0].max() + margin
    y_min, y_max = fit[:, 1].min() - margin, fit[:, 1].max() + margin
    xx, yy = np.meshgrid(np.arange(x_min, x_max, step),
                         np.arange(y_min, y_max, step))
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    figure = plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot the training points
    plt.scatter(fit[:, 0], fit[:, 1], c=classes, cmap=cmap_bold)
    for x, y in zip(fit[:, 0], fit[:, 1]):
        dx = +offset if x > 0 else -offset
        dy = +offset if y > 0 else -offset
        plt.text(x + dx, y + dy, f"({x}, {y})", fontsize=10)

    if predict:
        # Plot the testing points
        predict = list(dict.fromkeys(predict))
        predict = np.array([np.array(p) for p in predict])
        p_classes = knn.predict(predict)

        if connect:
            neighbors = knn.kneighbors(predict, return_distance=False)

        for i in range(len(predict)):
            x, y, c = predict[i][0], predict[i][1], p_classes[i]

            color = "blue" if c else "red"
            plt.scatter(x, y, c=color)
            dx = +offset if x > 0 else -offset
            dy = +offset if y > 0 else -offset
            plt.text(x + dx, y + dy, f"({x}, {y})", fontsize=10)

            if connect:
                colors = [classes[n] for n in neighbors[i]]
                neighbors = [fit[n] for n in neighbors[i]]

                for n, c in zip(neighbors, colors):
                    color = "b" if c else "r"
                    marker = f"{color}--"
                    plt.plot([x, n[0]], [y, n[1]], marker)

                    dx, dy = (n[0] + x) / 2, (n[1] + y) / 2
                    angle = degrees(atan2((dy - y), (dx - x)))
                    if abs(angle) > 90 and abs(angle) < 270:
                        angle += 180
                    angle = plt.gca().transData.transform_angles(
                        np.array((angle,)),
                        np.array((dx, dy)).reshape((1, 2))
                    )[0]
                    plt.text(
                        dx, dy,
                        f"{euclidean(n, (x, y)):.3f}",
                        fontsize=8,
                        rotation=angle, rotation_mode='anchor'
                    )

        plt.scatter(
            predict[:, 0], predict[:, 1],
            edgecolors="black", facecolors="none", s=48
        )

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title(title)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()

    if save or filename:
        if not filename:
            folder = path.join("images", path.splitext(__file__)[0])

            if not path.isdir(folder):
                makedirs(folder)

            filename = f"{title}"
            filename = filename.lower()
            filename = sub(r" |-|=|\(|\)|\{|\}|\!", "_", filename)
            filename = path.join(folder, f"{filename}.eps")

        figure.savefig(filename, format="eps")


if __name__ == "__main__":
    classify()
