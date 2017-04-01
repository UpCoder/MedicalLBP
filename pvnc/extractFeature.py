# -*- coding: utf-8 -*-
import os
import readFile
import numpy as np
import caluLBP as lbp
import wavelet.caluWavelet as wt
from sklearn import preprocessing
def extractFeature(dirPath):
    dirs = os.listdir(dirPath)
    allData = []
    allCountArr = []
    for singleDir in dirs:
        if singleDir.startswith('.'):
            continue
        artFileName = os.path.join(dirPath, singleDir, 'Tumor_New', 'Tumor_'+singleDir+"_ART.mhd")
        ncFileName = os.path.join(dirPath, singleDir, 'Tumor_New', 'Tumor_'+singleDir+"_NC.mhd")
        pvFileName = os.path.join(dirPath, singleDir, 'Tumor_New', 'Tumor_'+singleDir+"_PV.mhd")

        print artFileName
        artImages = readFile.readSingleFile(artFileName)
        ncImages = readFile.findUsefulImage(readFile.readSingleFile(ncFileName))
        pvImages = readFile.findUsefulImage(readFile.readSingleFile(pvFileName))
        [z1, y1, x1] = np.shape(ncImages)
        [z2, y2, x2] = np.shape(pvImages)
        if z1 < z2:
            pvImages = pvImages[0:z1][:][:]
        elif z1 > z2:
            ncImages = ncImages[0:z2][:][:]
        diffImages = (pvImages - ncImages)
        print 'diffImages size is ',np.shape(diffImages)
        diffImagesROI = readFile.caluROI(diffImages)
        print 'diffImagesROI size is ', np.shape(diffImagesROI)
        feature = []
        for singleImage in diffImagesROI:
            singleLine = []
            singleLine.extend(wt.caluSingleWavelet((singleImage), 5))
            print 'singleImage size is ', np.shape(singleImage)
            singleLine.extend(lbp.caluLBP2D(singleImage)[0][:])
            # print 'singleLine len is ', len(singleLine)
            feature.append(singleLine)
        print 'feature size is ', np.shape(feature)
        allData.extend(feature)
        allCountArr.append(np.shape(feature)[0])
        print 'feature size is ',np.shape(feature)
        print 'allData size is ', np.shape(allData)
    min_max_scaler = preprocessing.MinMaxScaler()
    allData[:][0:19] = min_max_scaler.fit_transform(allData[:][0:19])
    return allData, allCountArr
def imageRegistration(images1,images2):
    [z0, y0, x0] = np.shape(images1)
    [z1, y1, x1] = np.shape(images2)
    if z0 < z1:
        images = images1
        otherImages = images2
        z = z0
        zMax = z1
    else:
        z = z1
        zMax = z0
        images = images2
        otherImages = images1
    sameSizeImages = []
    for i in range(z):
        curImage = images[i, :, :]
        [x, y] = caluCeter(curImage)
        minDist = np.inf
        for j in range(zMax):
            curImage1 = otherImages[j, :, :]
            [x1, y1] = caluCeter(curImage1)
            if minDist > caluDist(x, y, x1, y1):
                minImage = curImage1
        sameSizeImages.append(minImage)
    return images,np.array(sameSizeImages)
def caluDist(x, y, x1, y1):
    return (x-x1)**2 + (y-y1)**2
def caluCeter(data):
    [m,n] = np.shape(data)
    xSum1 = 0.0
    xSum2 = 0.0
    ySum1 = 0.0
    ySum2 = 0.0
    for i in range(m):
        for j in range(n):
            xSum1 += ((i + 1) * data[i, j])
            xSum2 += data[i, j]
            ySum1 += ((j + 1) * data[i, j])
            ySum2 += data[i, j]
    return xSum1/xSum2, ySum1/ySum2
