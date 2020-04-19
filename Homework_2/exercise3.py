
from os import path, makedirs
from re import sub

import click
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier


@click.command()
@click.option("--neighbors", default=1, help="the number of neighbors to use")
@click.option("--metric", default='minkowski', help="the distance metric to use")
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
@click.option("--save", is_flag=True, help="save the resulting figure")
@click.option("--filename", default=None, help="where to save the resulting figure")
def classify(
    neighbors, metric, p,
    step, offset, margin,
    fit, classes, predict,
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
    cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#0000FF'])

    title = f"{neighbors}-NN Classification using the {metric} ({p}) metric"

    # We create an instance of Neighbours Classifier and fit the data.
    clf = KNeighborsClassifier(
        neighbors,
        weights='uniform',
        metric=metric,
        p=p
    )
    clf.fit(fit, classes)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = fit[:, 0].min() - margin, fit[:, 0].max() + margin
    y_min, y_max = fit[:, 1].min() - margin, fit[:, 1].max() + margin
    xx, yy = np.meshgrid(np.arange(x_min, x_max, step),
                            np.arange(y_min, y_max, step))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    figure = plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot the training points
    plt.scatter(fit[:, 0], fit[:, 1], c=classes, cmap=cmap_bold)
    for x, y in zip(fit[:, 0], fit[:, 1]):
        dx = +offset if x > 0 else -offset
        dy = +offset if y > 0 else -offset
        plt.text(x + dx, y + dy, '({}, {})'.format(x, y))

    if predict:
        # Plot the testing points
        predict = list(dict.fromkeys(predict))
        predict = np.array([np.array(p) for p in predict])
        classes = clf.predict(predict)

        for i in range(len(predict)):
            x, y, c = predict[i][0], predict[i][1], classes[i]
            color = 'blue' if c else 'red'
            plt.scatter(x, y, c=color)
            dx = +offset if x > 0 else -offset
            dy = +offset if y > 0 else -offset
            plt.text(x + dx, y + dy, '({}, {})'.format(x, y))
        plt.scatter(predict[:, 0], predict[:, 1], c='black', marker="x", s=16)

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title(title)

    plt.show()

    if save or filename:
        if not filename:
            folder = path.join("images", path.splitext(__file__)[0])

            if not path.isdir(folder):
                makedirs(folder)

            filename = f"{title}"
            filename = filename.lower()
            filename = sub(r' |-|=|\(|\)|\{|\}|\!', '_', filename)
            filename = path.join(folder, f"{filename}.eps")

        figure.savefig(filename, format="eps")

if __name__ == "__main__":
    classify()
