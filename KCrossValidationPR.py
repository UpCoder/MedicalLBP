from sklearn.model_selection import KFold
import numpy as np
import myKNN as knn
import myPrecisionRecall as pr
import mySVM as svm
import matplotlib.pyplot as plt
def kCrossValidation(allData,allLabel,trueLabel,countArr):
    kf = KFold(n_splits=5,shuffle=True)
    m = len(countArr)
    print 'm is ', m
    temp = np.zeros((m,1))
    for i in range(m):
        temp[i] = i
    accuracy = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    trueAccuracy = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    for train,test in kf.split(trueLabel):
        trainData, trainLabel, trainCountArr, trainTrueLabel, testData, testLabel, testCountArr, testTrueLabel = getTrainTestData(allData,allLabel,trueLabel,countArr,train,test)
        pr.myPR(trainData, trainLabel, trainTrueLabel,trainCountArr, testData, testLabel, testTrueLabel, testCountArr)
def getTrainTestData(allData,allLabel,trueLabel,countArr,trainIndexs,testIndexs):
    trainData = []
    trainLabel = []
    trainCountArr = []
    trainTrueLabel = []
    testData = []
    testCountArr = []
    testLabel = []
    testTrueLabel = []
    index = 0;
    for i in range(len(countArr)):
        if i in trainIndexs:
            # print 'trainIndex'
            trainTrueLabel.append(trueLabel[i])
            trainCountArr.append(countArr[i])
            for j in range(countArr[i]):
                trainData.append(allData[index][:])
                trainLabel.append(allLabel[index])

                index += 1
        elif i in testIndexs:
            # print 'testIndex'
            testTrueLabel.append(trueLabel[i])
            testCountArr.append(countArr[i])
            for j in range(countArr[i]):
                testData.append(allData[index][:])
                testLabel.append(allLabel[index])

                index += 1
        else:
            print 'error'
    return trainData, trainLabel, trainCountArr, trainTrueLabel, testData, testLabel, testCountArr, testTrueLabel

