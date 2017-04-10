# -*- coding: utf-8 -*-
import numpy as np
import math
from sklearn import preprocessing
from readFile import readSingleFile, caluROI
# image3D 三维的图像 d是距离
def calu3DGLCM(image3D,d):
    dirs = [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [1, 1, -1],
            [-1, 1, 1],
            [-1, 1, -1],
            [1, -1, 0],
            [1, 1, 0],
            [1, 0, 1],
            [1, 0, -1],
            [0, 1, 1],
            [0, 1, -1]]
    # 计算得到方向向量
    dirs = np.multiply(np.array(dirs), d)
    maxValue = np.max(image3D)
    minValue = np.min(image3D)
    maxDiff = math.sqrt(maxValue - minValue)
    # print 'maxDiff is ', maxDiff
    grayMatrix = np.zeros((maxDiff+2, maxDiff+2))  # 初始化矩阵值
    image3D = myNormalization3D(image3D, maxDiff, minValue=minValue, maxValue=maxValue) # 进行归一化，降低复杂度
    # print maxDiff
    # print np.max(image3D), np.min(image3D)

    [o, n, m] = np.shape(image3D)
    for index in range(13):
        curDir = dirs[index]
        for x in range(m):
            for y in range(n):
                for z in range(o):
                    newX = x+curDir[0]
                    newY = y+curDir[1]
                    newZ = z+curDir[2]
                    if xyzOK(newX, newY, newZ, m, n, o):
                        curGary = image3D[z, y, x]
                        newGary = image3D[newZ, newY, newX]
                        # print curGary, newGary
                        grayMatrix[curGary, newGary] += 1
                        grayMatrix[newGary, curGary] += 1
    return grayMatrix

def myNormalization3D(image3D,maxDiff, minValue, maxValue):
    min_max_scaler = preprocessing.MinMaxScaler()
    [z,y,x] = np.shape(image3D)
    for i in range(z):
        image3D[i, :, :] = myNormalization2D(image3D[i, :, :], float(maxDiff), minValue, maxValue)
    return image3D
def myNormalization2D(image,maxDiff,minValue,maxValue):
    # print 'maxDiff is ', maxDiff
    [m,n] = np.shape(image)
    for i in range(m):
        for j in range(n):
            curRate = float((image[i, j]-minValue))/(float(maxValue-minValue))
            # print curRate
            if int(round(maxDiff * curRate)) > (maxDiff+2):
                print 'errror Rate > 1', curRate, maxDiff, int(round(maxDiff * curRate))
            image[i, j] = int(round(maxDiff * curRate))
    return image
def xyzOK(x, y, z, m, n, o):
    res = True
    if x<0 or x >= m:
        res = False
        return res
    if y < 0 or y >= n:
        res = False
        return res
    if z < 0 or z >= o:
        res = False
        return res
    return res

# images = readSingleFile('D:\MedicalImage\Srr000\Tumor_New\Tumor_Srr000_ART.mhd')
# imageROI = caluROI(images)
# grayMatrix = calu3DGLCM(imageROI, 6)
# print grayMatrix
