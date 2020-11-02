import math
import random

# https://en.wikipedia.org/wiki/Normal_distribution
def normdf(x, mean, sd):
    var = float(sd)**2
    de = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/de

print("This is Part B problem 4 source code")
print("This code is using concept of single variable Gaussian Distribution ")
print()

# Input Precedure
# Ask user to select classifier
print("select the number that you want to use as a classifier")
print("1 : sepal length")
print("2 : sepal width")
print("3 : petal length")
print("4 : petal width")

select = int(input())-1
TotalResult = [[0,0,0] for _ in range(3)]
TempInput = []
f = open("iris.data","r")

#Input the data and add a tag of iris name
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

# Use 5-fold cross validation
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

#################################################################################
######################## Main Part of the Program ###############################
#################################################################################
    SetosaCnt = 0
    SetosaAvg = 0
    SetosaSDev = 0
    VersicolourCnt = 0
    VersicolourAvg = 0
    VersicolourSDev = 0
    VirginicaCnt = 0
    VirginicaAvg = 0
    VirginicaSDev = 0

    # Calculate average of data
    for train in TrainInput:
        if train[4] =='Setosa':
            SetosaAvg+=train[select]
            SetosaCnt+=1
        elif train[4] =='Versicolour':
            VersicolourAvg+=train[select]
            VersicolourCnt+=1
        else :
            VirginicaAvg+=train[select]
            VirginicaCnt+=1

    SetosaAvg /= SetosaCnt
    VersicolourAvg /= VersicolourCnt
    VirginicaAvg /= VirginicaCnt

    # Calculate standard deviation of data
    for train in TrainInput:
        if train[4] == 'Setosa':
            SetosaSDev+=math.pow((train[select]-SetosaAvg),2)
        elif train[4] == 'Versicolour':
            VersicolourSDev+=math.pow((train[select]-VersicolourAvg),2)
        else :
            VirginicaSDev+=math.pow((train[select]-VirginicaAvg),2)

    SetosaSDev/=SetosaCnt
    SetosaSDev = math.sqrt(SetosaSDev)

    VersicolourSDev/=VersicolourCnt
    VersicolourSDev = math.sqrt(VersicolourSDev)

    VirginicaSDev/=VirginicaCnt
    VirginicaSDev = math.sqrt(VirginicaSDev)

    # Print calculated average and standard deviation
    print("Setosa avg : "+str(round(SetosaAvg,4))+" Standard deviation : "+str(round(SetosaSDev,4)))
    print("Versicolour avg : "+str(round(VersicolourAvg,4))+" Standard deviation : "+str(round(VersicolourSDev,4)))
    print("Virginica avg : "+str(round(VirginicaAvg,4))+" Standrad deviation : "+str(round(VirginicaSDev,4)))

    PredictionResult = [[0, 0, 0] for _ in range(3)]
    # Validation step
    CorrectCnt = 0
    for val in ValInput:
        SetosaProbability = normdf(val[select],SetosaAvg,SetosaSDev)
        VersicolourProbability = normdf(val[select],VersicolourAvg,VersicolourSDev)
        VirginicaProbability = normdf(val[select],VirginicaAvg,VirginicaSDev)

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
