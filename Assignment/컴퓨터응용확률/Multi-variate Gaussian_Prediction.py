import math
import random
from numpy import *

# https://en.wikipedia.org/wiki/Multivariate_normal_distribution
# 위 문서에 제시된 방법대로 multi-variate Gaussian model을 구현하였습니다.

# Calculate covariance
def cov(x, y):
    Xavg, Yavg = sum(x)/len(x), sum(y)/len(y)
    Sum = 0
    for i in range(0,len(x)):
        Sum += (x[i] - Xavg)*(y[i] - Yavg)
    return Sum/(len(x) - 1)

# Calculate covariance matrix
def cov_mat(X):
    return array([[cov(X[0], X[0]), cov(X[0], X[1]), cov(X[0],X[2]), cov(X[0], X[3])],
                     [cov(X[1], X[0]), cov(X[1], X[1]), cov(X[1], X[2]), cov(X[1], X[3])],
                     [cov(X[2], X[0]), cov(X[2], X[1]), cov(X[2], X[2]), cov(X[2], X[3])],
                     [cov(X[3], X[0]), cov(X[3], X[1]), cov(X[3], X[2]), cov(X[3], X[3])]])

# Calculate probability according to Gaussian model
def Multi_Norm(var, mean, cov):
    size = len(var)
    # determinant를 계산하는 과정은 선형대수 과정이지
    # 컴퓨터 응용확률 과정이 아니라고 판단하여
    # numpy.linalg.det를 사용하였습니다.
    det = linalg.det(cov)
    norm_const = 1.0 / (math.pow((2*math.pi), float(size)/2) * math.pow(det,1.0/2) )
    x_mu = array(var - mean)
    inv = linalg.inv(cov)
    result = math.pow(math.e, -0.5 * dot(dot(x_mu, inv), x_mu.T))
    return norm_const * result

# Input Precedure #
TotalResult = [[0,0,0] for _ in range(3)]
TempInput = []
f = open("iris.data","r")

print("This is Part B problem 5 source code")
print("This code is using concept of multi - variate Gaussian Distribution")
print()

# Input the data and add a tag of iris name
for i in range(0, 150):
    line = f.readline()
    temp = line.split(',')
    del (temp[4])
    if i >= 0 and i < 50:
        temp.append('Setosa')
    elif i >= 50 and i < 100:
        temp.append('Versicolour')
    else:
        temp.append('Virginica')
    TempInput.append(temp)
f.close()
print("Data Input End")
random.shuffle(TempInput)
print("Data shuffle End")

# Used 5-fold cross validation for evaluation
for step in range(0,5):
    print("----------------------------------------------------------------")
    print("Step ",step+1)
    ValSubSetStart = step * 30
    ValSubSetEnd = (step+1) * 30
    print("From "+str(ValSubSetStart) +"th data to "+str(ValSubSetEnd-1)+"th data is validation subset")
    TrainInput = []
    ValInput = []
    for i in range(0,150):
        # if this is a validation subset
        temp = []
        if i >= ValSubSetStart and i < ValSubSetEnd :
            for j in range(0, 4):
                temp.append(float(TempInput[i][j]))
            temp.append(TempInput[i][4])
            ValInput.append(temp)

        # if this is a Train subset
        else :
            for j in range(0, 4):
                temp.append(float(TempInput[i][j]))
            temp.append(TempInput[i][4])
            TrainInput.append(temp)

###################################################################################
########################## Main Part of this Problem ##############################
###################################################################################

    # Create 2d list for store 4 variables (width, length of petal, sepal)
    SetosaVar = [[] for _ in range(4)]
    VersicolourVar = [[] for _ in range(4)]
    VirginicaVar = [[] for _ in range(4)]
    SetosaMean = [[] for _ in range(4)]
    VersicolourMean = [[] for _ in range(4)]
    VirginicaMean = [[] for _ in range(4)]

    # move data from input to 2d list to train model
    for train in TrainInput:
        if train[4] == 'Setosa':
            for i in range(0,4):
                SetosaVar[i].append(train[i])
        elif train[4] == 'Versicolour':
            for i in range(0,4):
                VersicolourVar[i].append(train[i])
        else :
            for i in range(0,4):
                VirginicaVar[i].append(train[i])

    # Calculate average value each feature
    for i in range(0,4):
        SetosaMean[i] = sum(SetosaVar[i])/len(SetosaVar[i])
        VersicolourMean[i] = sum(VersicolourVar[i]) / len(VersicolourVar[i])
        VirginicaMean[i] = sum(VirginicaVar[i]) / len(VirginicaVar[i])

    PredictionResult = [[0, 0, 0] for _ in range(3)]

    # Validation step
    CorrectCnt = 0
    for val in ValInput:
        realVal = array([val[0],val[1],val[2],val[3]])
        answer = val[4]

        # Calculate probability according to the Gaussian distribution
        SetosaProbability = Multi_Norm(realVal, array(SetosaMean),cov_mat(SetosaVar))
        VersicolourProbability = Multi_Norm(realVal, array(VersicolourMean),cov_mat(VersicolourVar))
        VirginicaProbability = Multi_Norm(realVal, array(VirginicaMean),cov_mat(VirginicaVar))

        MaxProbability = max(SetosaProbability, VersicolourProbability, VirginicaProbability)

        # if the prediction result is same to tag, then prediction is correct
        if MaxProbability == SetosaProbability and val[4] == 'Setosa':
            PredictionResult[0][0] += 1
        elif MaxProbability == VersicolourProbability and val[4] == 'Versicolour':
            PredictionResult[1][1] += 1
        elif MaxProbability == VirginicaProbability and val[4] == 'Virginica':
            PredictionResult[2][2] += 1
        elif val[4] == 'Setosa' and MaxProbability == VersicolourProbability:
            PredictionResult[0][1] += 1
        elif val[4] == 'Setosa' and MaxProbability == VirginicaProbability:
            PredictionResult[0][2] += 1
        elif val[4] == 'Versicolour' and MaxProbability == SetosaProbability:
            PredictionResult[1][0] += 1
        elif val[4] == 'Versicolour' and MaxProbability == VirginicaProbability:
            PredictionResult[1][1] += 1
        elif val[4] == 'Virginica' and MaxProbability == SetosaProbability:
            PredictionResult[2][0] += 1
        elif val[4] == 'Virginica' and MaxProbability == VersicolourProbability:
            PredictionResult[2][1] += 1

    for i in range(0, 3):
        for j in range(0, 3):
            TotalResult[i][j] += PredictionResult[i][j]
    print("Step" + str(step+1) + " Finish")

SetosaPrecision = TotalResult[0][0]/(TotalResult[0][0] + TotalResult[0][1] + TotalResult[0][2])
SetosaRecall = TotalResult[0][0]/(TotalResult[0][0] + TotalResult[1][0] + TotalResult[2][0])
VersicolourPrecision = TotalResult[1][1]/(TotalResult[1][0] + TotalResult[1][1] + TotalResult[1][2])
VersicolourRecall = TotalResult[1][1]/(TotalResult[0][1] + TotalResult[1][1] + TotalResult[2][1])
VirginicaPrecision = TotalResult[2][2]/(TotalResult[2][0] + TotalResult[2][1] + TotalResult[2][2])
VirginicaRecall = TotalResult[2][2]/(TotalResult[0][2] + TotalResult[1][2] + TotalResult[2][2])

print("----------------------------------------------------------------")
print("Precision for Setosa : "+str(SetosaPrecision) + " recall : "+str(SetosaRecall))
print("Precision for Versicolour : "+str(VersicolourPrecision) + " recall : "+str(VersicolourRecall))
print("Precision for Virginica : "+str(VirginicaPrecision) + " recall : "+str(VirginicaRecall))
print("----------------------------------------------------------------")

input("Press enter to exit ;)")
