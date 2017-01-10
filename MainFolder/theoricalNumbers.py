#Lambda x mi

lambda_ = 0
mi_ = 0
    
rho = 0
rho1 = 0
rho2 = 0
X = 0
X1 = 0
X2 = 0
Xr = 0
Xr1 = 0
Xr2 = 0

def calculateFormula(i):
    U = (rho*Xr)/(1 - rho)
    if i == 1:
        return round(U, decimal_house)
    if i == 2:
        return round(rho*Xr + U, decimal_house)
    if i == 3:
        return round(U, decimal_house)
    if i == 4:
        return round((X2 + U)/(1 - rho1), decimal_house)
    if i == 5:
        return round(U/(1 - rho1), decimal_house)
    if i == 6:
        return round(U, decimal_house)
    if i == 7:
        return round(X/(1 - rho), decimal_house)
    if i == 8:
        return round(X1/(1 - rho1), decimal_house)
    if i == 9:
        return round(rho1*Xr1/(1 - rho1), decimal_house)
    if i == 10:
        return round(X/(1 - rho), decimal_house)

decimal_house = 10
min_param = 2
max_param = 8
iter_param = 1

param_table = []
for i in range(min_param, max_param, iter_param):
    for j in range(min_param, max_param, iter_param):
        if i < j:
            param_table.append([i,j])
            
#param_table = [[10.0, 11.0]]            
finalResults = []
for j, item in enumerate(param_table):

    lambda_ = item[0]
    mi_ = item[1]
    
    rho = lambda_/mi_
    rho1 = lambda_/mi_
    rho2 = lambda_/mi_
    X = 1/mi_
    X1 = X
    X2 = X
    Xr = X**2/2*X
    Xr1 = X
    Xr2 = X
    
    results = []
    for i in range(1, 11):
        results.append(calculateFormula(i))
    finalResults.append(results)

print(finalResults)
