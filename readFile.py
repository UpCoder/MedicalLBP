from SimpleITK import SimpleITK as itk
import numpy as np
from skimage.feature import local_binary_pattern
from skimage import io,exposure
import matplotlib.pyplot as plt
import cv2
def readSingleFile(filePath):
    header = itk.ReadImage(filePath)
    image = itk.GetArrayFromImage(header)
    print type(image)
    return image
def findUsefulImage(image):
    [z, x, y] = np.shape(image)
    res = []
    for i in range(z):
        if sum(sum(image[i,:,:] != 0)) !=0:
            res.append(image[i,:,:])
    print len(res)
    res = np.array(res)
    print type(res)
    return res
def caluROI(image3D):
    indexs = np.where(image3D != 0)
    minX = np.min(indexs[:][2])
    maxX = np.max(indexs[:][2])
    minY = np.min(indexs[:][1])
    maxY = np.max(indexs[:][1])
    minZ = np.min(indexs[:][0])
    maxZ = np.max(indexs[:][0])
    print minX, maxX
    print minZ, maxZ
    imageROI = image3D[minZ:maxZ+1, minY:maxY+1, minX:maxX+1]
    return imageROI

def caluROI2D(image2D):
    indexs = np.where(image2D != 0)
    minY = np.min(indexs[:][1])
    maxY = np.max(indexs[:][1])
    minZ = np.min(indexs[:][0])
    maxZ = np.max(indexs[:][0])
    print minZ, maxZ
    imageROI = image2D[minZ:maxZ + 1, minY:maxY + 1]
    return imageROI
# images = readSingleFile('C:/Users/GIVE/Documents/MATLAB/MedicalImage/trainData/Srr100/Tumor_New/Tumor_Srr100_NC.mhd')
# usefulImage = findUsefulImage(images)
# roiImage = caluROI(images)
# print np.shape(images)
# print np.shape(usefulImage)
# print np.shape(roiImage)
# radius = 3
# n_points = 8 * radius
# lbp = local_binary_pattern(roiImage[1,:,:], n_points, radius,'uniform')
# lbpHist = np.histogram(lbp,bins=26)
# print lbpHist[0]
# print np.shape(lbpHist[0])
# print np.max(lbp) - np.min(lbp)
# plt.subplot(121)
# plt.imshow(lbp, cmap='gray')
# plt.subplot(122)
# plt.imshow(roiImage[1,:,:], cmap='gray')
# plt.show()