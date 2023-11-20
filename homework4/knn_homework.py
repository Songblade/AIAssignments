# -*- coding: utf-8 -*-
"""knn homework.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12iAwDFO1I1OATbQTZ1XlVgOavVbGm20r

Import the libraries math (for square root and absolute value) and pandas and numpy for reading csv files.
"""

import math
import pandas as pd
import numpy as np

"""Make an untagged vector, point, and two tagged vectors, data1 and data2:"""

point = [1, 0, 0, '?']  # (an unknown tag)
data1 = [1, 1, 1, 'M']
data2 = [1, 3, 0, 'F']

"""Write code to separate the data (X) from the tag (Y).  Your output should be:

The vector [1, 1, 1] has tag M

The vector [1, 3, 0] has tag F

"""

print("The vector ", data1[0:-1], " has tag ", data1[-1])

"""Now let's classify the point as either M or F.  We'll do this by setting k = 1 and using the Euclidean distance.
We'll define that as:"""


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        # print ('x is ' , x)
        num1 = float(instance1[x])
        num2 = float(instance2[x])
        distance = distance + pow(num1 - num2, 2)
    return math.sqrt(distance)


"""Now, find out the distance between data1 and point and data2 and point.
Output what the tag should be using euclideanDistance."""

print(euclideanDistance(data1, point, 3))

"""Now, let's get more data from a file, myFile.csv. This code will read it for us:"""

url = 'https://github.com/rosenfa/ai/blob/master/myFile.csv?raw=true'
# changed error_bad_lines to on_bad_lines for what I think is the same behavior
df = pd.read_csv(url, header=0, on_bad_lines="skip")
# put data in dataset without header line
dataset = np.array(df)

"""Show that you understand what you read by:

1. Printing the first two vectors in the file
2. Printing the Euclidean distance between those two vectors

Here is some code which I think might help get you on your way!
"""

print(len(dataset))
print(euclideanDistance(dataset[0], dataset[1], 3))

"""Now assume you have a new value for point:

[0,0,100]

How would you classify this vector using the Euclidean distance function given all of the vectors in the file?

In order to help here is a hint:  

We suggest defining some type of data struction to store different vectors' distances and their tags like this:
"""

point = [0, 0, 100]


class distClass:
    dist = -1  # distance of current point from test point
    tag = '-'  # tag of current point


"""You can then add vector distances like this:"""

eucDistances = []  # list of distances, will hold objects of type distClass

temp = dataset[1]
label = temp[-1]
d = euclideanDistance(point, temp, 3)
print("The distances between ", point, " and ", temp, " is ", str(d))
print(" and the label is " + label)
obj = distClass()  # one record's distance and tag
obj.dist = d
obj.tag = label
eucDistances.append(obj)

eucDistances[0].dist

"""and sort them like this:"""

eucDistances.sort(key=lambda x: x.dist)

"""Questions:

1. What is the label for point if k=1?
2. What is the label for point if k=3?
3. Would the result be different if we used a different distance function like Hamming or Manhattan?
"""

# Add code with functions that implement Hamming and Manhattan distances and test
# what the label will be for k=1 and k=3 for all possibilities
# (6 total: 2 Euclidean, 2 Hamming and 2 Manhattan)

"""Up until here is a simplified version of the homework.
Below here is the work for the part we will be checking as the basis of your grade:

Now let's look at some bigger files:

1. mytrain.csv (for training the model)
2. mytest.csv (for testing)
"""

url = 'https://github.com/rosenfa/ai/blob/master/mytrain.csv?raw=true'
train_data = np.array(pd.read_csv(url, header=0, on_bad_lines="skip"))
url = 'https://github.com/rosenfa/ai/blob/master/mytest.csv?raw=true'
test_data = np.array(pd.read_csv(url, header=0, on_bad_lines="skip"))

print(train_data.shape)  # number of records and features
print(train_data)

print(test_data.shape)  # number of records and features
print(test_data)

"""I hope by now you understand where we are going with this :)

Now implement the knn code with 3 different values for k:
1. k = 1
2. k = 7
3. k = 15

and at first use the Euclidean distance.
Classify each of the vectors in the test_data dataset using the training data from train_data.
Which value for k did the best?  What accuracy did it give you?

Now see if using Hamming or Manhattan distance give any better results for the same values of k.  

Once you are done, you should have a total of 9 different results:

1. Three results for the different value of k using the Euclidean Distance
2. Three results for the different value of k using the Hamming Distance
3. Three results for the different value of k using the Manhattan Distance

Hint: I strongly suggest you base yourself on the code you've seen until this point so you don't have to reinvent the wheel!
"""

# Add code here

"""Grade Basis:

80% for correct answers (and yes, there are possibilities that multiple answers are correct-- especially for cases of ties).

20% : Documentation and easily readable code

Please publish your final Notebook in your Github directory.

The homework assignment is due by November 20th at 11:59 PM.

"""
