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

    f1=[]
    errf1=[]
    f2=[]
    errf2=[]
    f3=[]
    errf3=[]
    f4=[]
    errf4=[]
    f5=[]
    errf5=[]
    f6=[]
    errf6=[]
    f7=[]
    errf7=[]
    f8=[]
    errf8=[]
    f9=[]
    errf9=[]
    f10=[]
    errf10=[]

    np.random.seed(129)
    bank = System("bank")

    if(politics==1):
        for i in range(lambda_init,lambda_end,lambda_step):
            for j in range(mi_init,mi_end,mi_step):
                if(j>i):

                    #generate the queues for analysis
                    bank.create_IN_Bubble(rate=i)
                    bank.create_WAIT_Bubble(policy="FCFS")
                    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
                    bank.create_OUT_Bubble(rate=j)
                    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)

                    bank.startSystem()
                    finalString = bank.saveInString()

                    for i in range(iterations):
                        finalString += bank.run_episode(printstates = True)

                    with open("file", "w") as f:
                        f.write(finalString)

                    #analysis of file
                    queue=parse.parseDo()
                    for i in queue:
                        parameters.updateQueue(i)
                    result=parameters.returnResults()

                    #generate array for print
                    lambda_par.append(i)
                    mi_par.append(j)
                    #numerical calculus
                    N.append(result[2][0])
                    errN.append(result[2][1])
                    N_q.appen(result[0][0])
                    errN_q.append(result[0][1])
                    N_q1.append(result[7][0])
                    errN_q1.append(result[7][1])
                    N_q2.appen(result[8][0])
                    errN_q2.appen(result[8][1])
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
                    errX_r.append(resut[6][1])
                    X_r1.append(result[12][0])
                    errX_r1.append(result[12][1])
                    X_r2.append(result[16][0])
                    errX_r2.append(result[16][1])
                    #formulas
                    ro=i/j

                    vMax=ro*(result[6][0]+result[6][1])/(1-ro)
                    vMin=ro*(result[6][0]-result[6][1])/(1-ro)
                    f1.append((vMax+vMin)/2)
                    errf1.append((vMax-vMin)/2)
#somente caso 1 e 2
                    vMax=ro*(result[6][0]+result[6][1])+(ro**2)*(result[5][0]+result[5][1])
                    vMin=ro*(result[6][0]-result[6][1])+(ro**2)*(result[5][0]-result[5][1])
                    f2.append((vMax+vMin)/2)
                    errf2.append((vMax-vMin)/2)

                    vMax=ro*(result[6][0]+result[6][1])/(1-ro)
                    vMin=ro*(result[6][0]-result[6][1])/(1-ro)
                    f3.append((vMax+vMin)/2)
                    errf3.append((vMax-vMin)/2)

                    vMax=(result[13][0]+result[13][1]+result[5][0]+result[5][1])/(1-ro)
                    vMin=(result[13][0]-result[13][1]+result[5][0]-result[5][1])/(1-ro)
                    f4.append((vMax+vMin)/2)
                    errf4.append((vMax-vMin)/2)

                    vMax=(result[5][0]+result[5][1])/(1-ro)
                    vMin=(result[5][0]-result[5][1])/(1-ro)
                    f5.append((vMax+vMin)/2)
                    errf5.append((vMax-vMin)/2)

                    f6.append(result[5][0])
                    errf6.append(result[5][1])

                    vMax=(result[3][0]+result[3][1])/(1-ro)
                    vMin=(result[3][0]-result[3][1])/(1-ro)
                    f7.append((vMax+vMin)/2)
                    errf7.append((vMax-vMin)/2)

                    vMax=(result[9][0]+result[9][1])/(1-ro)
                    vMin=(result[9][0]-result[9][1])/(1-ro)
                    f8.append((vMax+vMin)/2)
                    errf8.append((vMax-vMin)/2)

                    vMax=ro*(result[12][0]+result[12][1])/(1-ro)
                    vMin=ro*(result[12][0]-result[12][1])/(1-ro)
                    f9.append((vMax+vMin)/2)
                    errf9.append((vMax-vMin)/2)

                    vMax=(result[3][0]+result[3][1])/(1-ro)
                    vMin=(result[3][0]-result[3][1])/(1-ro)
                    f10.append((vMax+vMin)/2)
                    errf10.append((vMax-vMin)/2)

    elif(politics==2):
        pass

    elif(politics==3):
        pass

    elif(politics==4):
        pass

    elif(politics==5):
        pass

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

    ret.append(f1)
    ret.append(errf1)
    ret.append(f2)
    ret.append(errf2)
    ret.append(f3)
    ret.append(errf3)
    ret.append(f4)
    ret.append(errf4)
    ret.append(f5)
    ret.append(errf5)
    ret.append(f6)
    ret.append(errf6)
    ret.append(f7)
    ret.append(errf7)
    ret.append(f8)
    ret.append(errf8)
    ret.append(f9)
    ret.append(errf9)
    ret.append(f10)
    ret.append(errf10)

    return ret
