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
        ncFileName = os.path.join(dirPath, singleDir, 'Tumor_New', 'Tumor_' + singleDir + "_ART.mhd")
        print artFileName
        artImages = readFile.readSingleFile(artFileName)
        ncImages = readFile.readSingleFile(ncFileName)
        ncImagesROI = readFile.caluROI(ncImages)
        artImagesROI = readFile.caluROI(artImages)
        feature = lbp.caluLBP(artImagesROI)
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


