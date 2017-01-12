from parse import *
from analysis import *

if __name__ == "__main__":
    parse=Parse('fila')
    parameters=CalculateParameters()

    queue=parse.parseDo()

    for i in queue:
        parameters.updateQueue(i)

    result=parameters.returnResults()

    #print (queue)

    print("\n\n")

    print ('E[N]=%f +- %f\n' %(result[2][0] ,result[2][1]))
    print ('E[N_q]=%f +- %f\n' %(result[0][0] ,result[0][1]))
    print ('E[N_s]=%f +- %f\n' %(result[1][0] ,result[1][1]))
    print ('E[X]=%f +- %f\n' %(result[3][0] ,result[3][1]))
    print ('E[T]=%f +- %f\n' %(result[4][0] ,result[4][1]))
    print ('E[W]=%f +- %f\n' %(result[5][0] ,result[5][1]))
    print ('E[X_r]=%f +- %f\n' %(result[6][0] ,result[6][1]))
    print ('E[N_q1]=%f +- %f\n' %(result[7][0] ,result[7][1]))
    print ('E[N_q2]=%f +- %f\n' %(result[8][0] ,result[8][1]))
    print('\n')
    print ('E[X_1]=%f +- %f\n' %(result[9][0] ,result[9][1]))
    print ('E[T_1]=%f +- %f\n' %(result[10][0] ,result[10][1]))
    print ('E[W_1]=%f +- %f\n' %(result[11][0] ,result[11][1]))
    print ('E[X_r1]=%f +- %f\n' %(result[12][0] ,result[12][1]))
    print('\n')
    print ('E[X_2]=%f +- %f\n' %(result[13][0] ,result[13][1]))
    print ('E[T_2]=%f +- %f\n' %(result[14][0] ,result[14][1]))
    print ('E[W_2]=%f +- %f\n' %(result[15][0] ,result[15][1]))
    print ('E[X_r2]=%f +- %f\n' %(result[16][0] ,result[16][1]))
    print ('E[B]=%f +- %f\n' %(result[17][0] ,result[17][1]))
    print("\n")
