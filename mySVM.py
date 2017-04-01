# -*- coding: utf-8 -*-
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn import metrics
import numpy as np
def myKNN(data,label,testData,testLabel,testTrueLabel,countArr):
    accuracy = []
    trueAccuracy = []
    for i in range(9):
        # model = KNeighborsClassifier(n_neighbors=(i+1))
        # model.fit(data, label)
        # predictRes = model.predict(testData)
        clf = svm.SVC()
        clf.fit(data,label)
        predictRes = clf.predict(testData)
        accuracy.append(metrics.accuracy_score(testLabel, predictRes))
        index = 0
        errorCount = 0
        for i in range(len(countArr)):
            classifyMapping = [0,0,0,0,0]
            for j in range(countArr[i]):
                # print 'index is ',index
                classifyMapping[int(predictRes[index])-1] += 1
                index += 1
            indexs = getMaxIndexs(classifyMapping)
            flag = False
            for z in indexs:
                if z == testTrueLabel[i]:
                    flag = True
                    break
            if flag == False:
                print 'predicted error predicted:real:', indexs[0], ' : ', testTrueLabel[i]
                errorCount += 1
        trueAccuracy.append(1-((errorCount*1.0)/(len(countArr)*1.0)))  # 经过投票之后的结果的准确率
        print 'accuracy is ', accuracy
        print 'trueAccuracy is ',trueAccuracy
    return accuracy,trueAccuracy
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