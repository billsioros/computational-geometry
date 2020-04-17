from csv import reader
from exercise1 import KNearestNeighbor

import random


# helper function: dictionary: get key from value 
def get_species(flower_labels, flower_id): 
    for key, value in flower_labels.items(): 
         if flower_id == value: 
             return key 


# read dataset from csv file
# give appropriate delimiter and labels of dataset
def read_from_csv(filename, delimiter, labels):
    dataset = []
    with open(filename, 'r') as csv_file:
        csv_reader = reader(csv_file, delimiter=delimiter)
        header = next(csv_reader)  # avoid header of csv file
        if header == None:  # empty csv file
            return dataset
        else:
            for row in csv_reader:
                del row[0]  # remove id
                # change label from string to 0,1,2
                row.append(labels[row[-1]])
                del row[-2]  # remove string label
                for idx in range(len(row)):  # convert string data to float data
                    row[idx] = float(row[idx])
                dataset.append(row)
    return dataset


# dataset into k folds
def construct_folds(dataset, number_of_folds):
    records_per_fold = int(len(dataset) / number_of_folds)

    dataset_folds = []
    for i in range(number_of_folds):
        fold = []   # construct fold
        for j in range(records_per_fold):
            # pick random record for fold
            random_index = random.randrange(len(dataset))
            record = dataset[random_index]
            fold.append(record)
            del dataset[random_index]
        dataset_folds.append(fold)
    return dataset_folds


if __name__ == "__main__":
    # mark iris species with integer
    flower_labels = {
        'Iris-setosa': 0,
        'Iris-versicolor': 1,
        'Iris-virginica': 2
    }
    # read dataset
    dataset = read_from_csv("./Iris.csv", ',', flower_labels)

    # split dataset into folds
    number_of_folds = 3
    backup_dataset = dataset
    fold_dataset = construct_folds(
        backup_dataset, number_of_folds)  # split dataset

    # trainset
    trainset = [rec for fold in fold_dataset[:number_of_folds - 1]
        for rec in fold]

    # testset    
    testset = fold_dataset[-1]

    # k-NN
    number_of_neighboors = 10
    Knn = KNearestNeighbor(train=trainset, k=number_of_neighboors)
    prediction = Knn.get_predict(testset)

    # print predictions
    for i in range(len(testset)):
        print(f"Real flower specie is |{get_species(flower_labels, testset[i][-1])}| and k-NN predicted |{get_species(flower_labels, prediction[i])}|")    

    # accuracy
    Knn.accuracy_calc(testset, prediction)
    print(f"k-NN with k = {Knn.k} has Accuracy = {Knn.accuracy}")    
