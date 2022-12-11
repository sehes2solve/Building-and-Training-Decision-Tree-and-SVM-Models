import time
import numpy as np, pandas as pd, matplotlib as plt , random

alpha = 0.001
numberOfRuns = 1000
lamda = 1 / numberOfRuns


def terminals_train_test_split(x, y):
    if y.size != x.shape[0]:
        print('X size not same as Y Size')
        return
    trainingSet=0.2
    test_portion_half = np.ceil(y.size * trainingSet) / 2
    test_1st_idx = int(np.ceil(test_portion_half))
    test_2nd_idx = int(-np.floor(test_portion_half))
    x_train = x[test_1st_idx:test_2nd_idx]
    x_test = np.append(x[:test_1st_idx], x[test_2nd_idx:], axis=0)
    y_train = y[test_1st_idx:test_2nd_idx]
    y_test = np.append(y[:test_1st_idx], y[test_2nd_idx:])
    return x_train, x_test, y_train, y_test


def standradization(data):
    means = data.mean(axis=0)
    stds = data.std(axis=0)
    return (data - means) / stds, means, stds


def hyp(w, x):
    return x.dot(w)


def cost(y, x, w):
    calcY = hyp(w, x)
    sum = 0
    for i in range(0, len(y)):
        mul = y[i] * getClass(calcY[i])
        if (mul < 1):
            sum += 1 - mul

def getClass(val):
    if(val>0):
        return 1
    return -1

def gradient_direction(W, x, y):
    if(y * (np.dot(x, W)) >= 1 ):
        return -2 * alpha * lamda * W
    else:
        return alpha * (y * x - 2 * lamda * W)
def gradient_descent(x, y):
    W = np.zeros(len(x[0]))
    for j in range(0, numberOfRuns):
        for i in range(0, len(x)):
            W = W + gradient_direction(W, x[i], y[i])
    return W

def accuracy(W, x, y):
    predictions = hyp(W, x)
    correct_predictions = 0
    for i in range(y.size):
        if getClass(predictions[i]) == y[i]:
            correct_predictions += 1
    res=correct_predictions / y.size * 100
    return res

def fixData(lst):
    for row in lst:
        if (row[-1] == 0):
            row[-1] = -1

def solve(features):
    heart_data = pd.read_csv("heart.csv", usecols=features)
    numpy_lst = heart_data.to_numpy()
    fixData(numpy_lst)
    Xs = numpy_lst[:, :-1]
    onesCol = np.ones((len(Xs),1))
    # feature scaling
    Xs = standradization(Xs)[0]
    Xs = np.append(Xs,onesCol,axis=1)
    Ys = numpy_lst[:, -1]
    W = gradient_descent(Xs,Ys)
    return accuracy(W,Xs,Ys)

bestSet = ['sex', 'cp', 'chol', 'thalach', 'slope', 'ca', 'thal', 'target']
print(str(solve(bestSet)))
