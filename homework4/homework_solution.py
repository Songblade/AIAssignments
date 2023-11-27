# Due to everything that is happening in knn_homework, I'm not importing it so that I don't have to deal with its many
# prints and redundant

import math
import pandas as pd
import numpy as np


def euclidean_distance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        # print ('x is ' , x)
        num1 = float(instance1[x])
        num2 = float(instance2[x])
        distance = distance + pow(num1 - num2, 2)
    return math.sqrt(distance)


def manhattan_distance(instance1, instance2, length):
    # Using a pythonic method makes me cooler
    return sum(
        abs(float(instance1[i] - float(instance2[i])))
        for i in range(length)
    )


def hamming_distance(instance1, instance2, length):
    return sum(
        1 if instance1[i] != instance2[i] else 0
        for i in range(length)
    )


class DistPoint:
    dist = -1  # distance of current point from test point
    tag = '-'  # tag of current point

    # I wanted a constructor to make using it easier
    def __init__(self, dist, tag='-'):
        self.dist = dist
        self.tag = tag


'''
knn:
To determine the grouping of a new point:
For each point in the dataset, calculate the distance to the new point
Sort the points by distance
Choose the k closest points and check their tags
Return the most common tag
'''


# Note: This function assumes that the new_point has a tag at the end, even if it is blank
def knn(dataset, length, distance_function, k, new_point):
    # This list comprehension finds the length between 2 points, excluding the tag, and adds it to the list
    # Using point[-1] as the tag
    measured_points = [DistPoint(distance_function(point[:-1], new_point[:-1], length), point[-1])
                       for point in dataset]
    measured_points.sort(key=lambda x: x.dist)
    # Sums the number of male points among the first k points
    m_sum = sum(1 for point in measured_points[:k]
                if point.tag == 'M')

    return 'M' if m_sum > k/2 else 'F'  # If we have at least 50% male among the closest, return male, otherwise female


def run_knn(distance_function, k):
    # get the training and test data
    url = 'https://github.com/rosenfa/ai/blob/master/mytrain.csv?raw=true'
    train_data = np.array(pd.read_csv(url, header=0, on_bad_lines="skip"))
    url = 'https://github.com/rosenfa/ai/blob/master/mytest.csv?raw=true'
    test_data = np.array(pd.read_csv(url, header=0, on_bad_lines="skip"))

    length = 29

    print("Running knn for function " + distance_function.__name__ + " at k=" + str(k))

    accuracy_sum = 0
    for point in test_data:
        knn_value = knn(train_data, length, distance_function, k, point)
        # print("At point " + str(point[:-1]) + " knn returned " + str(knn_value) + " when the real value was " +
        #       str(point[-1]))
        accuracy_sum += 1 if knn_value == point[-1] else 0

    accuracy = accuracy_sum / len(test_data)
    print("Accuracy is " + str(accuracy))
    return accuracy


def display_results():
    # This is just testing knn
    max_accuracy = 0
    best_function = None
    best_k = 0
    for distance_function in (euclidean_distance, manhattan_distance, hamming_distance):
        for k in (1, 7, 15):
            accuracy = run_knn(distance_function, k)
            if accuracy > max_accuracy:
                max_accuracy = accuracy
                best_function = distance_function
                best_k = k
    print("The best accuracy is " + str(max_accuracy) + " with " + best_function.__name__ + " and k=" + str(best_k))


display_results()
