import numpy as np
from skimage.feature import local_binary_pattern
def caluLBP(images):
    [z,y,x] = np.shape(images)
    result = []
    for i in range(z):
        curImage = images[i, :, :]
        r = 3
        points = 8*3
        lbp = local_binary_pattern(curImage, points, r, 'uniform')
        hists = np.histogram(lbp, np.max(lbp)-np.min(lbp))

        allSum = np.sum(hists[0][0:-2])
        energy = []
        for j in range(len(hists[0])-1):
            energy.append(float((hists[0][j] * 1.0)/(allSum*1.0)))
        result.append(energy)
    print 'caluLBP size is ', np.shape(result)
    return result

