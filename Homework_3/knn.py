
import math
from abc import ABC, abstractmethod
from collections import Counter
from operator import itemgetter

import numpy as np
from scipy.spatial import KDTree

from decorators import benchmark


def accuracy(labels, prediction):
    successful_predictions = sum([
        labels[i] == prediction[i]
        for i in range(len(labels))
    ])

    return successful_predictions / len(labels)


class KNN(ABC):
    @staticmethod
    def normalize(instances):
        min_feature = []
        max_feature = []

        for i in range(len(instances[0])):
            column = []
            for instance in instances:
                column.append(instance[i])

            min_feature.append(min(column))
            max_feature.append(max(column))

        normalized_instances = []
        for instance in instances:
            normalized_instance = [0] * len(instance)

            for i in range(len(instance)):
                num = float(instance[i] - min_feature[i])
                den = float(max_feature[i] - min_feature[i])
                normalized_instance[i] = num / den

            normalized_instances.append(normalized_instance)

        return normalized_instances

    def __init__(self, n_neighbors=3, p=2):
        self.n_neighbors = n_neighbors
        self.p = p

    def label(self, neighbors):
        labels = [self.labels[i] for i in neighbors]

        return Counter(labels).most_common()[0][0]

    @abstractmethod
    def fit(self, data, labels):
        self.data = self.normalize(data)
        self.labels = labels

    @abstractmethod
    def predict(self, test_instances):
        return self.normalize(test_instances)


class KNNForce(KNN):

    def minkowski(self, a, b):
        return math.sqrt(sum([
            pow(a[i] - b[i], self.p) for i in range(len(a))
        ]))

    def neighbours(self, test_instance):
        distances = [
            (
                i,
                self.minkowski(self.data[i], test_instance)
            )
            for i in range(len(self.data))
        ]

        sorted_distances = sorted(distances, key=itemgetter(1))
        sorted_training_instances = [tuple[0] for tuple in sorted_distances]

        return sorted_training_instances[:self.n_neighbors]

    @benchmark
    def fit(self, data, labels):
        super().fit(data, labels)

    @benchmark
    def predict(self, test_instances):
        test_instances = super().predict(test_instances)

        return np.array([
            self.label(self.neighbours(test_instance))
            for test_instance in test_instances
        ])


class KNNTree(KNN):
    def __init__(self, n_neighbors=3, p=2):
        super().__init__(n_neighbors=n_neighbors, p=p)

    @benchmark
    def fit(self, data, labels):
        super().fit(data, labels)

        self.kdtree = KDTree(self.data)

    @benchmark
    def predict(self, test_instances):
        test_instances = super().predict(test_instances)

        _, groups = self.kdtree.query(
            test_instances, k=self.n_neighbors, p=self.p
        )

        return np.array([
            self.label([
                indices[i] for i in range(self.n_neighbors)
            ]) if isinstance(indices, list) else self.labels[indices]
            for indices in groups
        ])


if __name__ == '__main__':
    dataset = [
        [0.23, 4.75],
        [1.75, 3.93],
        [2.05, 3.11],
        [4.83, 3.52],
        [4.92, 1.93],
        [7.23, 11.85],
        [10.36, 6.52],
        [7.58, 11.77],
        [10.79, 10.53],
        [8.43, 9.64]
    ]

    labels = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

    test = [
        [4.77, 0.55],
        [10.22, 10.33]
    ]

    test_labels = [0, 1]

    for cls in [KNNForce, KNNTree]:
        print(f'Class: {cls.__name__}')

        knn = cls()
        knn.fit(dataset, labels)

        prediction = knn.predict(test)

        for i in range(len(test)):
            print(
                f'Label: {test_labels[i]:02d}, '
                f'Prediction: {prediction[i]:02d}'
            )

        print(f'Accuracy: {accuracy(test_labels, prediction)}\n')
