TrainingSet = [
    [1, 1, 1, 1],
    [1, -1, 1, -1],
    [-1, 1, 1, -1],
    [-1, -1, 1, -1]
]

w1, w2, b = 0, 0, 0
a = 0.01

Expected_Error = 0.01
epoch = 1
while True:
    Error = 0
    for i in range(len(TrainingSet)):
        Y_NI = b + (w1 * TrainingSet[i][0]) + (w2 * TrainingSet[i][1])
        if Y_NI >= 0:
            Y_NI = 1
        else:
            Y_NI = -1
        Delta_w1 = a * (TrainingSet[i][3] - Y_NI) * TrainingSet[i][0]
        Delta_w2 = a * (TrainingSet[i][3] - Y_NI) * TrainingSet[i][1]
        Delta_b  = a * (TrainingSet[i][3] - Y_NI) * 1
        w1 += Delta_w1
        w2 += Delta_w2
        b += Delta_b
        Error += (TrainingSet[i][3] - Y_NI) * (TrainingSet[i][3] - Y_NI)
    
    epoch += 1
    if Error <= Expected_Error:
        break
    

x1, x2 = map(int, input().split())
y = b + (w1 * x1) + (w2 * x2)
if y >= 0:
    print(1)
else:
    print(-1)

print("epoch: " + str(epoch))