# -*- coding: utf-8 -*-
import os
import readFile
import numpy as np
import caluLBP as lbp
def extractFeature(dirPath):
    dirs = os.listdir(dirPath)
    allData = []
    allCountArr = []
    for singleDir in dirs:
        if singleDir.startswith('.'):
            continue
        artFileName = os.path.join(dirPath, singleDir, 'Tumor_New', 'Tumor_'+singleDir+"_ART.mhd")
        print artFileName
        artImages = readFile.readSingleFile(artFileName)
        artImagesROI = readFile.caluROI(artImages)
        feature = lbp.caluLBP(artImagesROI)
        # for i in range(np.shape(artImagesROI)[0]):
        #    curSingleImage = artImagesROI[i, :, :]
        #    curSingleImage = readFile.caluROI2D(curSingleImage)
        #    singleFeature = lbp.caluLBP2D(curSingleImage)
        #    feature.extend(singleFeature)
        #print 'feature size is ', np.shape(feature)
        #for x in range(len(feature)):
        #    allData.append(feature[x])
        allData.extend(feature)
        allCountArr.append(np.shape(feature)[0])
        print 'feature size is ',np.shape(feature)
        print 'allData size is ', np.shape(allData)
    return allData, allCountArr
def imageRegistration(images1,images2):
    [z0,y0,x0] = np.shape(images1)
    [z1,y1,x1] = np.shape(images2)
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
def caluDist(x,y,x1,y1):
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



