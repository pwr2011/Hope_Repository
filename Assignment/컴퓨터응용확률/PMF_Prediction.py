import random

# Input Precedure
print("This is Part B problem 3 source code")
print("This code is using concept of pmf of likelihood")
print()
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

    # Make a list to count the mass distribution
    SetosaDistribution = []
    VersicolourDistribution = []
    VirginicaDistribution = []
    for i in range(0, 100):
        SetosaDistribution.append(0)
        VersicolourDistribution.append(0)
        VirginicaDistribution.append(0)

    # Count the mass distribution
    for train in TrainInput:
        if train[4] == 'Setosa':
            SetosaDistribution[int(train[select]*10)] += 1
        elif train[4] == 'Versicolour':
            VersicolourDistribution[int(train[select] * 10)] += 1
        else:
            VirginicaDistribution[int(train[select] * 10)] += 1

    print("finding pmf end")

    # prior define
    SetosaPrior = 1/3
    VersicolourPrior = 1/3
    VirginicaPrior = 1/3

    # create list to calculate precision-recall
    # This list is thought like this
    ########################################################
    #    Predict \Real |  Setosa Versicolour  Virginica
    #           Setosa |
    #      Versicolour |
    #        Virginica |
    ########################################################
    PredictionResult = [[0,0,0] for _ in range(3)]

    # Validate the model
    for val in ValInput:
        # Calcuate the probability of each class
        # posterior = likelihood * prior
        #           =     pmf    * prior
        SetosaProbability = SetosaDistribution[int(val[select]*10)]/sum(SetosaDistribution)*SetosaPrior
        VersicolourProbability = VersicolourDistribution[int(val[select]*10)]/sum(VersicolourDistribution)*VersicolourPrior
        VirginicaProbability = VirginicaDistribution[int(val[select])*10]/sum(VirginicaDistribution)*VirginicaPrior

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

    for i in range(0,3):
        for j in range(0,3):
            TotalResult[i][j] += PredictionResult[i][j]
    print("Step"+str(step+1)+" Finish")

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
