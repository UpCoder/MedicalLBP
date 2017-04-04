# -*- coding: utf-8 -*-
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import Queue
import numpy as np
import math
def myPR(data,label,trainTrueLabel,trainCountArr,testData,testLabel,testTrueLabel,testCountArr):
    accuracy = []
    trueAccuracy = []
    trainTrueData = getAverage(data, trainCountArr)
    testTrueData = getAverage(testData, testCountArr)
    precisions = []
    for i in range(10):
        print 'start select ', i+1
        targets = i + 1
        precision = 0.0
        for index, singleTest in enumerate(testTrueData):
            myArr = caluDists(trainTrueData, singleTest, targets)
            targetLabel = testTrueLabel[index]
            count = 0
            for line in myArr:
                print 'trainTrueLabel Index is ', line[1]
                print 'predict:real:', trainTrueLabel[line[1]], targetLabel
                if trainTrueLabel[line[1]] == targetLabel:
                    count += 1
            precision += ((1.0*count)/float(len(myArr)))
        precision = precision/float(len(testTrueData))
        precisions.append(precision)
    print 'precision is ', precisions
def caluDists(data,test,targetNum):
    myArr = []
    for index, line in enumerate(data):
        dist = caluSingleDist(line, test)
        if len(myArr) < targetNum:
            myArr.append([dist, index])
            continue
        sorted(myArr, cmp=numeric_compare)
        # print 'the lien is ',myArr[targetNum-1]
        if dist < myArr[targetNum-1][0]:
            myArr[targetNum-1] = [dist, index]
    return myArr
def numeric_compare(x,y):
    [dist, index] = x
    [dist1, index1] = y
    return int(dist-dist1)
def caluSingleDist(x,y):
    res = 0.0
    # print 'x is ', x
    # print 'y is ', y
    for i in range(len(x)):
        res += (x[0][i]-y[0][i])**2
    # print 'single dist is ', res
    return math.sqrt(res)
def getMaxIndexs(arr):
    indexs = []
    values = -np.inf
    for i in range(len(arr)):
        if arr[i] > values:
            indexs = []
            indexs.append(i+1)
            values = arr[i]
        #elif arr[i] == values:
        #    indexs.append(i+1)
    return indexs
def getAverage(data,countArr):
    res = []
    index = 0
    [m, n] = np.shape(data)
    for i in range(len(countArr)):
        line = np.zeros((1, n))
        for j in range(countArr[i]):
            line += data[index][:]
            index += 1
        line /= countArr[i]
        res.append(line)
    return res