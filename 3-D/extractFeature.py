# -*- coding: utf-8 -*-
import os
import readFile
import numpy as np
import cv2
import scipy.io as sci
from sklearn import preprocessing
import calu3DGLCM as GLCM
import math
def extractFeature(dirPath):
    dirs = os.listdir(dirPath)
    allData = []
    allCountArr = []
    for singleDir in dirs:
        if singleDir.startswith('.'):
            continue

        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        artFileName = os.path.join(dirPath, singleDir, 'Tumor_New', 'Tumor_'+singleDir+"_ART.mhd")
        print artFileName
        artImages = readFile.readSingleFile(artFileName)
        artImagesROI = readFile.caluROI(artImages)
        artImagesROI1 = cv2.erode(artImagesROI, kernel1)
        artImagesROI2 = cv2.erode(artImagesROI, kernel2)

        ncFileName = os.path.join(dirPath, singleDir, 'Tumor_New', 'Tumor_'+singleDir+"_NC.mhd")
        print ncFileName
        ncImages = readFile.readSingleFile(ncFileName)
        ncImagesROI = readFile.caluROI(ncImages)
        ncImagesROI1 = cv2.erode(ncImagesROI, kernel1)
        ncImagesROI2 = cv2.erode(ncImagesROI, kernel2)

        pvFileName = os.path.join(dirPath, singleDir, 'Tumor_New', 'Tumor_'+singleDir+"_PV.mhd")
        print pvFileName
        pvImages = readFile.readSingleFile(pvFileName)
        pvImageROI = readFile.caluROI(pvImages)
        pvImageROI1 = cv2.erode(pvImageROI, kernel1)
        pvImageROI2 = cv2.erode(pvImageROI, kernel2)

        feature = []
        feature1 = []
        feature1.append(caluSingleF1(ncImagesROI))  # 0
        feature1.append(caluSingleF1(ncImagesROI1))  # 1
        feature1.append(caluSingleF1(ncImagesROI2))  # 2
        feature1.append(caluSingleF1(artImagesROI))  # 3
        feature1.append(caluSingleF1(artImagesROI1))  # 4
        feature1.append(caluSingleF1(artImagesROI2))  # 5
        feature1.append(caluSingleF1(pvImageROI))  # 6
        feature1.append(caluSingleF1(pvImageROI1))  # 7
        feature1.append(caluSingleF1(pvImageROI2))  # 8

        feature2 = []
        feature2.append(caluSingleF2(feature1[3], feature1[0]))
        feature2.append(caluSingleF2(feature1[4], feature1[1]))
        feature2.append(caluSingleF2(feature1[5], feature1[2]))
        feature2.append(caluSingleF2(feature1[6], feature1[0]))
        feature2.append(caluSingleF2(feature1[7], feature1[1]))
        feature2.append(caluSingleF2(feature1[8], feature1[2]))

        feature3 = []
        d = 6
        artGLCM = GLCM.calu3DGLCM(artImagesROI, d)
        artGLCM1 = GLCM.calu3DGLCM(artImagesROI1, d)
        artGLCM2 = GLCM.calu3DGLCM(artImagesROI2, d)

        ncGLCM = GLCM.calu3DGLCM(ncImagesROI, d)
        ncGLCM1 = GLCM.calu3DGLCM(ncImagesROI1, d)
        ncGLCM2 = GLCM.calu3DGLCM(ncImagesROI2, d)

        pvGLCM = GLCM.calu3DGLCM(pvImageROI, d)
        pvGLCM1 = GLCM.calu3DGLCM(pvImageROI1, d)
        pvGLCM2 = GLCM.calu3DGLCM(pvImageROI2, d)


        feature3.extend(caluSingleF3(ncGLCM)) # 0~5
        feature3.extend(caluSingleF3(ncGLCM1)) # 6~11
        feature3.extend(caluSingleF3(ncGLCM2)) # 12~17
        feature3.extend(caluSingleF3(artGLCM)) # 18~23
        feature3.extend(caluSingleF3(artGLCM1)) # 24~29
        feature3.extend(caluSingleF3(artGLCM2)) # 30~35
        feature3.extend(caluSingleF3(pvGLCM)) # 36~41
        feature3.extend(caluSingleF3(pvGLCM1)) # 42~47
        feature3.extend(caluSingleF3(pvGLCM2)) # 48~53

        feature4 = []
        feature4.extend(np.subtract(feature3[18:24], feature3[36:42]))  # 0~5
        feature4.extend(np.subtract(feature3[24:30], feature3[42:48]))  # 6~11
        feature4.extend(np.subtract(feature3[30:36], feature3[48:54]))  # 12~17

        # 0~8
        feature.extend(feature1)
        # 9~14
        feature.extend(feature2)
        # 15~68
        feature.extend(feature3)
        # 69 ~ 86
        feature.extend(feature4)
        allData.append(feature)
        allCountArr.append(1)
        # for singleImage in artImagesROI:
        #     singleLine = []
        #     singleLine.extend(wt.caluSingleWavelet(readFile.caluROI2D(singleImage), 5))
        #     singleLine.extend(lbp.caluLBP2D(singleImage)[0][:])
        #     # print 'singleLine len is ', len(singleLine)
        #     feature.append(singleLine)
        #     # print 'feature len is ', len(feature), len(feature[0])
        # #for x in range(len(feature)):
        # #    allData.append(feature[x])
        # print 'feature size is ', np.shape(feature)
        # allData.extend(feature)
        # allCountArr.append(np.shape(feature)[0])
        # print 'feature size is ',np.shape(feature)
        # print 'allData size is ', np.shape(allData)
    # min_max_scaler = preprocessing.MinMaxScaler()
    # allData[:][0:19] = min_max_scaler.fit_transform(allData[:][0:19])
    sci.savemat('allData.mat', {'allData': allData, 'allCountArr': allCountArr})
    print np.shape(allData)
    allData = np.array(allData)
    print np.shape(allData)

    for i in range(2):
        for j in range(87):
            print allData[i, j], ' ',
        print '\n'
    startValue = 0.0
    endValue = 1.0
    # feature1
    allData[:, 0:9] = myNormalization(allData[:, 0:9], startValue, endValue)
    curIndex = 9
    # feature 2
    for i in range(9, 15):
        allData[:, curIndex] = myNormalization1(allData[:, curIndex], startValue, endValue)
        curIndex += 1
    # feature 3
    indexs = [15, 21, 27, 33, 39, 45, 51, 57, 63]
    print allData[:, indexs]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)
    print allData[:, indexs]
    indexs = [16, 22, 28, 34, 40, 46, 52, 58, 64]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    indexs = [17, 23, 29, 35, 41, 47, 53, 59, 65]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    indexs = [18, 24, 30, 36, 42, 48, 54, 60, 66]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    indexs = [19, 25, 31, 37, 43, 49, 55, 61, 67]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    indexs = [20, 26, 32, 38, 44, 50, 56, 62, 68]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    # feature 4
    indexs = [69, 75, 81]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    indexs = [70, 76, 82]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    indexs = [71, 77, 83]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    indexs = [72, 78, 84]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    indexs = [73, 79, 85]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    indexs = [74, 80, 86]
    allData[:, indexs] = myNormalization(allData[:, indexs], startValue, endValue)

    print 'after normalization'
    for i in range(2):
        for j in range(87):
            print allData[i, j], ' ',
        print '\n'
    return allData, allCountArr
def caluSingleF1(images):
    return np.sum(images)
# return (x-y)/y
def caluSingleF2(x,y):
    x = float(x)
    y = float(y)
    return (float(x-y)/y)
def caluSingleF3(glcm):
    res = []
    t1 = 0.0
    t2 = 0.0
    t3 = 0.0
    t4 = 0.0
    t5 = 0.0
    t6 = 0.0
    [m, n] = np.shape(glcm)
    # for i in range(m):
    #     for j in range(n):
    #         print glcm[i, j], ' ',
    #     print '\n'
    ui = []
    uj = []
    ci = []
    cj = []
    for i in range(m):
        sum = 0.0
        for j in range(n):
            sum += glcm[i, j]
        ui.append(i*sum)
    for j in range(n):
        sum = 0.0
        for i in range(m):
            sum += glcm[i, j]
        uj.append(j * sum)

    for i in range(m):
        sum = 0.0
        for j in range(n):
            sum += glcm[i, j]
        ci.append(math.pow((i-ui[i]), 2)*sum)

    for j in range(n):
        sum = 0.0
        for i in range(m):
            sum += glcm[i, j]
        cj.append(math.pow((j - uj[j]), 2) * sum)
    for i in range(m):
        for j in range(n):
            t1 += math.pow(glcm[i, j], 2)
            if glcm[i, j] != 0:
                t2 += glcm[i, j] * math.log(glcm[i, j])
            t3 += float(glcm[i, j]) / float(1+math.pow((i-j), 2))
            t4 += math.pow((i-j), 2) * glcm[i, j]
            t5 += math.pow((i+j-ui[i]-uj[j]), 3) * glcm[i, j]
            if ci[i] !=0 and cj[j] != 0:
                t6 += ((i-ui[i]) * (j-uj[j]) * glcm[i,j])/(ci[i] * cj[j])
    res.append(t1)
    res.append(t2)
    res.append(t3)
    res.append(t4)
    res.append(t5)
    res.append(t6)
    # print 'res is ', res
    return res
def myNormalization(image,start,end):
    maxValue = np.max(image)
    minValue = np.min(image)
    maxDiff = end - start
    [m, n] = np.shape(image)
    for i in range(m):
        for j in range(n):
            curRate = float((image[i, j]-minValue))/(float(maxValue-minValue))
            # print 'curRate is', curRate
            image[i, j] = maxDiff * curRate + start
    return image
def myNormalization1(image,start,end):
    maxValue = np.max(image)
    minValue = np.min(image)
    maxDiff = end - start
    m = len(image)
    for i in range(m):
        curRate = float((image[i]-minValue))/(float(maxValue-minValue))
        # print curRate
        image[i] = maxDiff * curRate + start
    return image