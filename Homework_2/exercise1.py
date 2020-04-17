#########################################################
#   k-Nearest Neighbor implementation from scratch      #
#           basic main for running k-NN                 #
#########################################################

from operator import itemgetter
from collections import Counter
import matplotlib.pyplot as plt

import numpy as np
import math

labels_color = {
    0: "g",
    1: "b"
}


# plot dataset of points at 2D
def plot_2D_points(points, test_points, labels_color):
    fig, ax = plt.subplots()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    # set position of x spine to x=0
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    # set position of y spine to y=0
    ax.spines['left'].set_position(('data', 0))

    plt.title("k-Nearest Neighbor")
    for point in test_points:
        plt.scatter(point[0], point[1], color="r")

    for point in points:
        plt.scatter(point[0], point[1], color=labels_color[point[2]])
        # plt.text(point[0]+0.2, point[1]+0.2, f'({point[0]},{point[1]})' , fontsize=11)

    plt.show()


class KNearestNeighbor:

    def __init__(self, train, k=5, accuracy=None):
        self.k = k
        self.train = train

    # Euclidean distance between 2 vectors
    def get_distance(self, data1, data2):
        distance = 0
        data1 = data1[:len(data1) - 1]
        for idx, val in enumerate(data1):
            distance += pow(data1[idx] - data2[idx], 2)
        return math.sqrt(distance)

    # getting neighbours
    def get_neighbours(self, test_instance):
        distances = [self.get_tuple_distance(
            training_instance, test_instance) for training_instance in self.train]
        sorted_distances = sorted(distances, key=itemgetter(1))
        sorted_training_instances = [tuple[0] for tuple in sorted_distances]
        return sorted_training_instances[:self.k]

    # private method to convert to tuple instance and its distance
    def get_tuple_distance(self, training_instance, test_instance):
        return (training_instance, self.get_distance(test_instance, training_instance))

   # getting majority vote (selects category with the most votes)
    def get_majority_vote(self, neighbours):
        categories = [neighbour[-1] for neighbour in neighbours]
        # print(f"Categories: {categories}")
        count = Counter(categories)
        # print(f"count: {count}")
        return count.most_common()[0][0]

    # predicting
    def get_predict(self, test_instances):
        self.train = self.normalization(self.train)
        test_instances = self.normalization(test_instances)
        # plot_2D_points(self.train, test_instances, labels_color)
        predictions = []
        for x in range(len(test_instances)):
            neighbours = self.get_neighbours(test_instance=test_instances[x])
            majority_vote = self.get_majority_vote(neighbours)
            predictions.append(majority_vote)
        return predictions

    # calculate accuracy of knn algorithm
    def accuracy_calc(self, test_fold, prediction):
        labels_test_fold = [record[-1]
                            for record in test_fold]  # labels of test set
        successful_prediction = 0
        for idx, val in enumerate(labels_test_fold):
            if labels_test_fold[idx] == prediction[idx]:
                successful_prediction += 1
        self.accuracy = successful_prediction / \
            float(len(labels_test_fold)) * 100.0

    # normalization routine for train and test dataset
    def normalization(self, instances):
        min_feature = []
        max_feature = []
        feature_row = instances[0]
        feature_row = feature_row[:len(feature_row) - 1]
        for i, val in enumerate(feature_row):
            column = []
            for feature in instances:
                column.append(feature[i])
            min_feature.append(min(column))
            max_feature.append(max(column))
        for row in instances:
            feature_row = row[:len(row) - 1]
            for i, val in enumerate(feature_row):
                num = float(row[i] - min_feature[i])
                den = float(max_feature[i] - min_feature[i])
                row[i] = num / den
        return instances

    def get_params(self):
        return {"train": self.train, "k": self.k, "accuracy": self.accuracy}


if __name__ == "__main__":
    dataset = [[0.23, 4.75, 0],
               [1.75, 3.93, 0],
               [2.05, 3.11, 0],
               [4.83, 3.52, 0],
               [4.92, 1.93, 0],
               [7.23, 11.85, 1],
               [10.36, 6.52, 1],
               [7.58, 11.77, 1],
               [10.79, 10.53, 1],
               [8.43, 9.64, 1]]
    test = [[4.77, 0.55, 0],
            [10.22, 10.33, 1]]

    # plot test data with red and train data with blue and green
    plot_2D_points(dataset, test, labels_color)

    # k-Nearest Neighbor
    Knn = KNearestNeighbor(train=dataset, k=3)
    prediction = Knn.get_predict(test)

    # print predictions
    for i, val in enumerate(test):
        print(
            f"Label of test data is {test[i][-1]} and k-NN predict {prediction[i]}")
