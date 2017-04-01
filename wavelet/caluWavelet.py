# -*- coding: utf-8 -*-
import numpy as np
import pywt as wt
def caluWavelet3D(images,n):
    [z, y, x] = np.shape(images)
    res = []
    for i in range(z):
        curImage = images[i, :, :]
        singleWavelet = caluSingleWavelet(curImage,n)
        res.append(singleWavelet)
    return res
# data 是图像数据二维的，n是进行几次小波变换
def caluSingleWavelet(data,n):
    #data = np.ones((4, 4), dtype=np.float64)
    result = []
    for i in range(n):
        # print 'data size is '
        # print np.shape(data)
        coffess = wt.dwt2(data,'haar')
        CA,(CH,CV,CD) = coffess
        # print 'CA size is '
        # print np.shape(CA)
        result.append(caluWaveletPacketEnergy(CA))
        result.append(caluWaveletPacketEnergy(CH))
        result.append(caluWaveletPacketEnergy(CV))
        result.append(caluWaveletPacketEnergy(CD))
        data = CA
    return result
def caluWaveletPacketEnergy(image):
    # print np.shape(image)
    [m, n] = np.shape(image)
    res = 0.0
    for i in range(m):
        for j in range(n):
            res += (image[i,j]**2)
    res = (1.0*res)/(1.0*m*n)
    return res