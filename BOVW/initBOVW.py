import cv2
import scipy as sp
import numpy as np

image1 = cv2.imread('D:\\lean.jpg')
sift = cv2.SIFT()
kp1,des1 = SIFT.detectAndCompute(image1,None)
print np.shape(kp1), np.shape(des1)