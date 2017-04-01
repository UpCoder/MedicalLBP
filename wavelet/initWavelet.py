from extractFeature import extractFeature as EF
import numpy as np
import kCrossValidation as KCV
def initLBP():
    dirPath = 'D:\\MedicalImage'
    allData,allCountArr = EF(dirPath)
    label1_1 = (np.ones((18, 1)))
    label1_2 = (np.ones((18, 1)))

    label2_1 = (np.ones((10, 1))*2)
    label2_2 = (np.ones((12, 1)) * 2)

    label3_1 = (np.ones((10, 1))*3)
    label3_2 = (np.ones((17, 1)) * 3)

    label4_1 = (np.ones((10, 1))*4)
    label4_2 = (np.ones((17, 1))*4)

    label5_1 = (np.ones((10, 1))*5)
    label5_2 = (np.ones((10, 1)) * 5)
    label = np.concatenate((label1_1, label2_1, label3_1, label4_1, label5_1,\
                            label1_2, label2_2, label3_2, label4_2, label5_2))
    # label = np.concatenate((label1_1, label2_1, label3_1,\
    #                         label1_2, label2_2, label3_2,))
    print 'first line is ', np.shape(allData[0][:])
    print allData[0][:]
    allLabel = getAllLabel(label, allCountArr)
    print 'allCountArr is ', allCountArr
    print  'allCountArr len is ', len(allCountArr)
    print 'allCountArr is ', np.sum(allCountArr)
    KCV.kCrossValidation(allData, allLabel, label, countArr=allCountArr)

def getAllLabel(label,allCountArr):
    result = []
    for i in range(np.shape(label)[0]):
        curNum = allCountArr[i]
        for j in range(curNum):
            result.append(label[i][0])
    result = np.array(result)
    print type(result)
    return result
initLBP()