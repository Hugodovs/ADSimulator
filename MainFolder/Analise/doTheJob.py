from bubble import *
from parse import *
from analysis import *


def doTheJob(politics=1,lambda_init=1,lambda_end=10,lambda_step=1,mi_init=1,mi_end=10,mi_step=1,iterations=1000):
    parse=Parse('fila')
    parameters=CalculateParameters()

    ret=[]
    lambda_par=[]
    mi_par=[]
    N=[]
    errN=[]
    N_q=[]
    errN_q=[]
    N_q1=[]
    errN_q1=[]
    N_q2=[]
    errN_q2=[]
    N_s=[]
    errN_s=[]
    X=[]
    errX=[]
    X_1=[]
    errX_1=[]
    X_2=[]
    errX_2=[]
    T=[]
    errT=[]
    T_1=[]
    errT_1=[]
    T_2=[]
    errT_2=[]
    W=[]
    errW=[]
    W_1=[]
    errW_1=[]
    W_2=[]
    errW_2=[]
    X_r=[]
    errX_r=[]
    X_r1=[]
    errX_r1=[]
    X_r2=[]
    errX_r2=[]
    B=[]
    errB=[]
    U=[]
    errU=[]

    f1=[]
    f2=[]
    f3=[]
    f4=[]
    f5=[]
    f6=[]
    f7=[]
    f8=[]
    f9=[]
    f10=[]

    if(politics==1):
        for i in range(lambda_init,lambda_end,lambda_step):
            for j in range(mi_init,mi_end,mi_step):
                if(j>i):

                    np.random.seed(129)
                    bank = System("bank")
                    #generate the queues for analysis
                    bank.create_IN_Bubble(ratePar=i)
                    bank.create_WAIT_Bubble(policy="FCFS")
                    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
                    bank.create_OUT_Bubble(ratePar=j)
                    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)

                    bank.startSystem()
                    finalString = bank.saveInString()

                    for k in range(iterations):
                        finalString += bank.run_episode(printstates = True)

                    with open("fila", "w") as f:
                        f.write(finalString)

                    #analysis of file
                    queue=parse.parseDo()
                    for l in queue:
                        parameters.updateQueue(l)
                    result=parameters.returnResults()

                    #generate array for print
                    lambda_par.append(i)
                    mi_par.append(j)
                    #numerical calculus
                    N.append(result[2][0])
                    errN.append(result[2][1])
                    N_q.append(result[0][0])
                    errN_q.append(result[0][1])
                    N_q1.append(result[7][0])
                    errN_q1.append(result[7][1])
                    N_q2.append(result[8][0])
                    errN_q2.append(result[8][1])
                    N_s.append(result[1][0])
                    errN_s.append(result[1][1])
                    X.append(result[3][0])
                    errX.append(result[3][1])
                    X_1.append(result[9][0])
                    errX_1.append(result[9][1])
                    X_2.append(result[13][0])
                    errX_2.append(result[13][1])
                    T.append(result[4][0])
                    errT.append(result[4][1])
                    T_1.append(result[10][0])
                    errT_1.append(result[10][1])
                    T_2.append(result[14][0])
                    errT_2.append(result[14][1])
                    W.append(result[5][0])
                    errW.append(result[5][1])
                    W_1.append(result[11][0])
                    errW_1.append(result[11][1])
                    W_2.append(result[15][0])
                    errW_2.append(result[15][1])
                    X_r.append(result[6][0])
                    errX_r.append(result[6][1])
                    X_r1.append(result[12][0])
                    errX_r1.append(result[12][1])
                    X_r2.append(result[16][0])
                    errX_r2.append(result[16][1])
                    B.append(result[17][0])
                    errB.append(result[17][1])
                    U.append(result[18][0])
                    errU.append(result[18][1])
                    #formulas

                    rho_analitical = i/j
                    rho1_analitical = i/j
                    rho2_analitical = i/j
                    X_analitical= 1/j
                    X1_analitical = X_analitical
                    X2_analitical = X_analitical
                    Xr_analitical = X_analitical**2/2*X_analitical
                    Xr1_analitical = X_analitical
                    Xr2_analitical = X_analitical
                    U_analitical = (rho_analitical*Xr_analitical)/(1 - rho_analitical)
                    decimal_house=10

                    f1.append(round(U_analitical, decimal_house))
                    f2.append(round(rho_analitical*Xr_analitical + U_analitical, decimal_house))
                    f3.append(round(U_analitical, decimal_house))
                    f4.append(round((X2_analitical + U_analitical)/(1 - rho1_analitical), decimal_house))
                    f5.append(round(U_analitical/(1 - rho1_analitical), decimal_house))
                    f6.append(round(U_analitical, decimal_house))
                    f7.append(round(X_analitical/(1 - rho_analitical), decimal_house))
                    f8.append(round(X1_analitical/(1 - rho1_analitical), decimal_house))
                    f9.append(round(rho1_analitical*Xr1_analitical/(1 - rho1_analitical), decimal_house))
                    f10.append(round(X_analitical/(1 - rho_analitical), decimal_house))


                    parameters.reinitQueue()

    elif(politics==2):
        for i in range(lambda_init,lambda_end,lambda_step):
            for j in range(mi_init,mi_end,mi_step):
                if(j>i):

                    np.random.seed(129)
                    bank = System("bank")
                    #generate the queues for analysis
                    bank.create_IN_Bubble(ratePar=i)
                    bank.create_WAIT_Bubble(policy="LCFS")
                    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
                    bank.create_OUT_Bubble(ratePar=j)
                    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)

                    bank.startSystem()
                    finalString = bank.saveInString()

                    for k in range(iterations):
                        finalString += bank.run_episode(printstates = True)

                    with open("fila", "w") as f:
                        f.write(finalString)

                    #analysis of file
                    queue=parse.parseDo()
                    for l in queue:
                        parameters.updateQueue(l)
                    result=parameters.returnResults()

                    #generate array for print
                    lambda_par.append(i)
                    mi_par.append(j)
                    #numerical calculus
                    N.append(result[2][0])
                    errN.append(result[2][1])
                    N_q.append(result[0][0])
                    errN_q.append(result[0][1])
                    N_q1.append(result[7][0])
                    errN_q1.append(result[7][1])
                    N_q2.append(result[8][0])
                    errN_q2.append(result[8][1])
                    N_s.append(result[1][0])
                    errN_s.append(result[1][1])
                    X.append(result[3][0])
                    errX.append(result[3][1])
                    X_1.append(result[9][0])
                    errX_1.append(result[9][1])
                    X_2.append(result[13][0])
                    errX_2.append(result[13][1])
                    T.append(result[4][0])
                    errT.append(result[4][1])
                    T_1.append(result[10][0])
                    errT_1.append(result[10][1])
                    T_2.append(result[14][0])
                    errT_2.append(result[14][1])
                    W.append(result[5][0])
                    errW.append(result[5][1])
                    W_1.append(result[11][0])
                    errW_1.append(result[11][1])
                    W_2.append(result[15][0])
                    errW_2.append(result[15][1])
                    X_r.append(result[6][0])
                    errX_r.append(result[6][1])
                    X_r1.append(result[12][0])
                    errX_r1.append(result[12][1])
                    X_r2.append(result[16][0])
                    errX_r2.append(result[16][1])
                    B.append(result[17][0])
                    errB.append(result[17][1])
                    U.append(result[18][0])
                    errU.append(result[18][1])
                    #formulas
                    rho_analitical = i/j
                    rho1_analitical = i/j
                    rho2_analitical = i/j
                    X_analitical= 1/j
                    X1_analitical = X_analitical
                    X2_analitical = X_analitical
                    Xr_analitical = X_analitical**2/2*X_analitical
                    Xr1_analitical = X_analitical
                    Xr2_analitical = X_analitical
                    U_analitical = (rho_analitical*Xr_analitical)/(1 - rho_analitical)
                    decimal_house=10

                    f1.append(round(U_analitical, decimal_house))
                    f2.append(round(rho_analitical*Xr_analitical + U_analitical, decimal_house))
                    f3.append(round(U_analitical, decimal_house))
                    f4.append(round((X2_analitical + U_analitical)/(1 - rho1_analitical), decimal_house))
                    f5.append(round(U_analitical/(1 - rho1_analitical), decimal_house))
                    f6.append(round(U_analitical, decimal_house))
                    f7.append(round(X_analitical/(1 - rho_analitical), decimal_house))
                    f8.append(round(X1_analitical/(1 - rho1_analitical), decimal_house))
                    f9.append(round(rho1_analitical*Xr1_analitical/(1 - rho1_analitical), decimal_house))
                    f10.append(round(X_analitical/(1 - rho_analitical), decimal_house))

                    parameters.reinitQueue()

    elif(politics==3):
        for i in range(lambda_init,lambda_end,lambda_step):
            for j in range(mi_init,mi_end,mi_step):
                if(j>i):

                    np.random.seed(129)
                    bank = System("bank")
                    #generate the queues for analysis

                    bank.create_IN_Bubble(ratePar=i)
                    bank.create_WAIT_Bubble(policy="FCFS")
                    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
                    bank.create_OUT_Bubble(ratePar=j,preemption=True)
                    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)

                    bank.startSystem()
                    finalString = bank.saveInString()

                    for k in range(iterations):
                        finalString += bank.run_episode(printstates = True)

                    with open("fila", "w") as f:
                        f.write(finalString)

                    #analysis of file
                    queue=parse.parseDo()
                    for l in queue:
                        parameters.updateQueue(l)
                    result=parameters.returnResults()

                    #generate array for print
                    lambda_par.append(i)
                    mi_par.append(j)
                    #numerical calculus
                    N.append(result[2][0])
                    errN.append(result[2][1])
                    N_q.append(result[0][0])
                    errN_q.append(result[0][1])
                    N_q1.append(result[7][0])
                    errN_q1.append(result[7][1])
                    N_q2.append(result[8][0])
                    errN_q2.append(result[8][1])
                    N_s.append(result[1][0])
                    errN_s.append(result[1][1])
                    X.append(result[3][0])
                    errX.append(result[3][1])
                    X_1.append(result[9][0])
                    errX_1.append(result[9][1])
                    X_2.append(result[13][0])
                    errX_2.append(result[13][1])
                    T.append(result[4][0])
                    errT.append(result[4][1])
                    T_1.append(result[10][0])
                    errT_1.append(result[10][1])
                    T_2.append(result[14][0])
                    errT_2.append(result[14][1])
                    W.append(result[5][0])
                    errW.append(result[5][1])
                    W_1.append(result[11][0])
                    errW_1.append(result[11][1])
                    W_2.append(result[15][0])
                    errW_2.append(result[15][1])
                    X_r.append(result[6][0])
                    errX_r.append(result[6][1])
                    X_r1.append(result[12][0])
                    errX_r1.append(result[12][1])
                    X_r2.append(result[16][0])
                    errX_r2.append(result[16][1])
                    B.append(result[17][0])
                    errB.append(result[17][1])
                    U.append(result[18][0])
                    errU.append(result[18][1])
                    #formulas
                    rho_analitical = i/j
                    rho1_analitical = i/j
                    rho2_analitical = i/j
                    X_analitical= 1/j
                    X1_analitical = X_analitical
                    X2_analitical = X_analitical
                    Xr_analitical = X_analitical**2/2*X_analitical
                    Xr1_analitical = X_analitical
                    Xr2_analitical = X_analitical
                    U_analitical = (rho_analitical*Xr_analitical)/(1 - rho_analitical)
                    decimal_house=10

                    f1.append(round(U_analitical, decimal_house))
                    f2.append(round(rho_analitical*Xr_analitical + U_analitical, decimal_house))
                    f3.append(round(U_analitical, decimal_house))
                    f4.append(round((X2_analitical + U_analitical)/(1 - rho1_analitical), decimal_house))
                    f5.append(round(U_analitical/(1 - rho1_analitical), decimal_house))
                    f6.append(round(U_analitical, decimal_house))
                    f7.append(round(X_analitical/(1 - rho_analitical), decimal_house))
                    f8.append(round(X1_analitical/(1 - rho1_analitical), decimal_house))
                    f9.append(round(rho1_analitical*Xr1_analitical/(1 - rho1_analitical), decimal_house))
                    f10.append(round(X_analitical/(1 - rho_analitical), decimal_house))

                    parameters.reinitQueue()

    elif(politics==4):
        for i in range(lambda_init,lambda_end,lambda_step):
            for j in range(mi_init,mi_end,mi_step):
                if(j>i):

                    np.random.seed(129)
                    bank = System("bank")
                    #generate the queues for analysis

                    bank.create_IN_Bubble(typePerson = "1",ratePar=i)
                    bank.create_IN_Bubble(typePerson = "2",ratePar=i)
                    bank.create_WAIT_Bubble(policy="FCFS", priority=[1,2])
                    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
                    bank.connect("IN_Bubble", 1, "WAIT_Bubble", 0)
                    bank.create_OUT_Bubble(ratePar=j)
                    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)

                    bank.startSystem()
                    finalString = bank.saveInString()

                    for k in range(iterations):
                        finalString += bank.run_episode(printstates = True)

                    with open("fila", "w") as f:
                        f.write(finalString)

                    #analysis of file
                    queue=parse.parseDo()
                    for l in queue:
                        parameters.updateQueue(l)
                    result=parameters.returnResults()

                    #generate array for print
                    lambda_par.append(i)
                    mi_par.append(j)
                    #numerical calculus
                    N.append(result[2][0])
                    errN.append(result[2][1])
                    N_q.append(result[0][0])
                    errN_q.append(result[0][1])
                    N_q1.append(result[7][0])
                    errN_q1.append(result[7][1])
                    N_q2.append(result[8][0])
                    errN_q2.append(result[8][1])
                    N_s.append(result[1][0])
                    errN_s.append(result[1][1])
                    X.append(result[3][0])
                    errX.append(result[3][1])
                    X_1.append(result[9][0])
                    errX_1.append(result[9][1])
                    X_2.append(result[13][0])
                    errX_2.append(result[13][1])
                    T.append(result[4][0])
                    errT.append(result[4][1])
                    T_1.append(result[10][0])
                    errT_1.append(result[10][1])
                    T_2.append(result[14][0])
                    errT_2.append(result[14][1])
                    W.append(result[5][0])
                    errW.append(result[5][1])
                    W_1.append(result[11][0])
                    errW_1.append(result[11][1])
                    W_2.append(result[15][0])
                    errW_2.append(result[15][1])
                    X_r.append(result[6][0])
                    errX_r.append(result[6][1])
                    X_r1.append(result[12][0])
                    errX_r1.append(result[12][1])
                    X_r2.append(result[16][0])
                    errX_r2.append(result[16][1])
                    B.append(result[17][0])
                    errB.append(result[17][1])
                    U.append(result[18][0])
                    errU.append(result[18][1])
                    #formulas
                    rho_analitical = i/j
                    rho1_analitical = i/j
                    rho2_analitical = i/j
                    X_analitical= 1/j
                    X1_analitical = X_analitical
                    X2_analitical = X_analitical
                    Xr_analitical = X_analitical**2/2*X_analitical
                    Xr1_analitical = X_analitical
                    Xr2_analitical = X_analitical
                    U_analitical = (rho_analitical*Xr_analitical)/(1 - rho_analitical)
                    decimal_house=10

                    f1.append(round(U_analitical, decimal_house))
                    f2.append(round(rho_analitical*Xr_analitical + U_analitical, decimal_house))
                    f3.append(round(U_analitical, decimal_house))
                    f4.append(round((X2_analitical + U_analitical)/(1 - rho1_analitical), decimal_house))
                    f5.append(round(U_analitical/(1 - rho1_analitical), decimal_house))
                    f6.append(round(U_analitical, decimal_house))
                    f7.append(round(X_analitical/(1 - rho_analitical), decimal_house))
                    f8.append(round(X1_analitical/(1 - rho1_analitical), decimal_house))
                    f9.append(round(rho1_analitical*Xr1_analitical/(1 - rho1_analitical), decimal_house))
                    f10.append(round(X_analitical/(1 - rho_analitical), decimal_house))

                    parameters.reinitQueue()

    elif(politics==5):
        for i in range(lambda_init,lambda_end,lambda_step):
            for j in range(mi_init,mi_end,mi_step):
                if(j>i):

                    np.random.seed(129)
                    bank = System("bank")
                    #generate the queues for analysis

                    bank.create_IN_Bubble(typePerson = "1",ratePar=i)
                    bank.create_IN_Bubble(typePerson = "2",ratePar=i)
                    bank.create_WAIT_Bubble(policy="FCFS", priority=[1,2])
                    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
                    bank.connect("IN_Bubble", 1, "WAIT_Bubble", 0)
                    bank.create_OUT_Bubble(ratePar=j, preemption=True)
                    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)

                    bank.startSystem()
                    finalString = bank.saveInString()

                    for k in range(iterations):
                        finalString += bank.run_episode(printstates = True)

                    with open("fila", "w") as f:
                        f.write(finalString)

                    #analysis of file
                    queue=parse.parseDo()
                    for l in queue:
                        parameters.updateQueue(l)
                    result=parameters.returnResults()

                    #generate array for print
                    lambda_par.append(i)
                    mi_par.append(j)
                    #numerical calculus
                    N.append(result[2][0])
                    errN.append(result[2][1])
                    N_q.append(result[0][0])
                    errN_q.append(result[0][1])
                    N_q1.append(result[7][0])
                    errN_q1.append(result[7][1])
                    N_q2.append(result[8][0])
                    errN_q2.append(result[8][1])
                    N_s.append(result[1][0])
                    errN_s.append(result[1][1])
                    X.append(result[3][0])
                    errX.append(result[3][1])
                    X_1.append(result[9][0])
                    errX_1.append(result[9][1])
                    X_2.append(result[13][0])
                    errX_2.append(result[13][1])
                    T.append(result[4][0])
                    errT.append(result[4][1])
                    T_1.append(result[10][0])
                    errT_1.append(result[10][1])
                    T_2.append(result[14][0])
                    errT_2.append(result[14][1])
                    W.append(result[5][0])
                    errW.append(result[5][1])
                    W_1.append(result[11][0])
                    errW_1.append(result[11][1])
                    W_2.append(result[15][0])
                    errW_2.append(result[15][1])
                    X_r.append(result[6][0])
                    errX_r.append(result[6][1])
                    X_r1.append(result[12][0])
                    errX_r1.append(result[12][1])
                    X_r2.append(result[16][0])
                    errX_r2.append(result[16][1])
                    B.append(result[17][0])
                    errB.append(result[17][1])
                    U.append(result[18][0])
                    errU.append(result[18][1])
                    #formulas
                    rho_analitical = i/j
                    rho1_analitical = i/j
                    rho2_analitical = i/j
                    X_analitical= 1/j
                    X1_analitical = X_analitical
                    X2_analitical = X_analitical
                    Xr_analitical = X_analitical**2/2*X_analitical
                    Xr1_analitical = X_analitical
                    Xr2_analitical = X_analitical
                    U_analitical = (rho_analitical*Xr_analitical)/(1 - rho_analitical)
                    decimal_house=10

                    f1.append(round(U_analitical, decimal_house))
                    f2.append(round(rho_analitical*Xr_analitical + U_analitical, decimal_house))
                    f3.append(round(U_analitical, decimal_house))
                    f4.append(round((X2_analitical + U_analitical)/(1 - rho1_analitical), decimal_house))
                    f5.append(round(U_analitical/(1 - rho1_analitical), decimal_house))
                    f6.append(round(U_analitical, decimal_house))
                    f7.append(round(X_analitical/(1 - rho_analitical), decimal_house))
                    f8.append(round(X1_analitical/(1 - rho1_analitical), decimal_house))
                    f9.append(round(rho1_analitical*Xr1_analitical/(1 - rho1_analitical), decimal_house))
                    f10.append(round(X_analitical/(1 - rho_analitical), decimal_house))

                    parameters.reinitQueue()

    ret.append(lambda_par)
    ret.append(mi_par)
    ret.append(N)
    ret.append(errN)
    ret.append(N_q)
    ret.append(errN_q)
    ret.append(N_q1)
    ret.append(errN_q1)
    ret.append(N_q2)
    ret.append(errN_q2)
    ret.append(N_s)
    ret.append(errN_s)
    ret.append(X)
    ret.append(errX)
    ret.append(X_1)
    ret.append(errX_1)
    ret.append(X_2)
    ret.append(errX_2)
    ret.append(T)
    ret.append(errT)
    ret.append(T_1)
    ret.append(errT_1)
    ret.append(T_2)
    ret.append(errT_2)
    ret.append(W)
    ret.append(errW)
    ret.append(W_1)
    ret.append(errW_1)
    ret.append(W_2)
    ret.append(errW_2)
    ret.append(X_r)
    ret.append(errX_r)
    ret.append(X_r1)
    ret.append(errX_r1)
    ret.append(X_r2)
    ret.append(errX_r2)
    ret.append(B)
    ret.append(errB)

    ret.append(f1)
    ret.append(f2)
    ret.append(f3)
    ret.append(f4)
    ret.append(f5)
    ret.append(f6)
    ret.append(f7)
    ret.append(f8)
    ret.append(f9)
    ret.append(f10)

    return ret
