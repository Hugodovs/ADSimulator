import math

#class that receive states of a queue and calculate individualy usefull quantities
#like /ro, E[U], E[X_r]...
class CalculateParameters:
    def __init__(self):
        #self.N=0
        self.N_q=0
        self.N_s=0
        self.T=0
        self.X=0
        self.W=0
        self.X_r=0
        self.X_2=0
        self.counter=0
        self.counterTime=0
        self.lastT=0
        self.allQueues=[]
        self.lastOut=-1
        self.times=[]
        self.N_q1=0
        self.N_q2=0

        self.W_1=0
        self.W_2=0
        self.T_1=0
        self.T_2=0
        self.X_1=0
        self.X_1_2=0
        self.X_2=0
        self.X_2_2=0
        self.X_r1=0
        self.X_r2=0
        self.times1=[]
        self.times2=[]
        self.counterTime1=0
        self.counterTime2=0

    #function that receive a new state of queue and update the parameters
    def updateQueue(self,queue):
        #calculate N_q and N_s only if T differs from 0
        if self.counter!=0:
            self.N_q+=len(queue[3])*(queue[0][0]-self.lastT)
            counter1=0
            counter2=0
            for q1 in queue[3]:
                if q1[0]==1:
                    counter1+=1
                elif q1[0]==2:
                    counter2+=1
            self.N_q1+=counter1*(queue[0][0]-self.lastT)
            self.N_q2+=counter2*(queue[0][0]-self.lastT)
            if len(queue[4])>0:
                self.N_s+=(queue[0][0]-self.lastT)

        #calculate T, X and W and X_r
        if len(queue[4])>0 and queue[4][0]!=self.lastOut:
            self.X_2+=(queue[4][3])**2
            self.X+=queue[4][3]
            self.T+=queue[4][4]-queue[4][2]
            self.W+=queue[4][4]-queue[4][2]-queue[4][3]
            self.times.append([queue[4][3],queue[4][4]-queue[4][2],queue[4][4]-queue[4][2]-queue[4][3],(queue[4][3])**2])

            if(queue[4][0]==1):
                self.X_1_2+=(queue[4][3])**2
                self.X_1+=queue[4][3]
                self.T_1+=queue[4][4]-queue[4][2]
                self.W_1+=queue[4][4]-queue[4][2]-queue[4][3]
                self.times1.append([queue[4][3],queue[4][4]-queue[4][2],queue[4][4]-queue[4][2]-queue[4][3],(queue[4][3])**2])
                self.counterTime1+=1
            elif(queue[4][0]==2):
                self.X_2_2+=(queue[4][3])**2
                self.X_2+=queue[4][3]
                self.T_2+=queue[4][4]-queue[4][2]
                self.W_2+=queue[4][4]-queue[4][2]-queue[4][3]
                self.times2.append([queue[4][3],queue[4][4]-queue[4][2],queue[4][4]-queue[4][2]-queue[4][3],(queue[4][3])**2])
                self.counterTime2+=1

            self.lastOut=queue[4][1]
            self.counterTime+=1

        self.counter+=1
        self.lastT=queue[0][0]
        self.allQueues.append(queue)

    #function that return the final values calculated
    def returnResults(self):
        if self.counter==0:
            return []

        ret=[]

        #N_q and interval calculation
        conf=0
        N_q=self.N_q/self.lastT
        for i in self.allQueues:
            conf+=(len(i[3])-N_q)**2
        conf/=(len(self.allQueues)-1)
        conf=1.96*conf/math.sqrt(len(self.allQueues))
        ret.append([N_q,conf])

        #N_s and interval calculation
        conf=0
        N_s=self.N_s/self.lastT
        for i in self.allQueues:
            if(len(i[4])>0):
                conf+=(1-N_s)**2
            else:
                conf+=N_s**2
        conf/=(len(self.allQueues)-1)
        conf=1.96*conf/math.sqrt(len(self.allQueues))
        ret.append([N_s,conf])

        #N and interval calculation
        conf=0
        N=(self.N_q+self.N_s)/self.lastT
        for i in self.allQueues:
            if(len(i[4])>0):
                conf+=(len(i[2])+1-N)**2
            else:
                conf+=(len(i[2])-N)**2
        conf/=(len(self.allQueues)-1)
        conf=1.96*conf/math.sqrt(len(self.allQueues))
        ret.append([N,conf])

        #X and interval calculation
        conf=0
        X=self.X/self.counterTime
        for i in self.times:
            conf+=(i[0]-X)**2
        conf/=(len(self.times)-1)
        conf=1.96*conf/math.sqrt(len(self.times))
        ret.append([X,conf])

        #T and interval calculation
        conf=0
        T=self.T/self.counterTime
        for i in self.times:
            conf+=(i[1]-T)**2
        conf/=(len(self.times)-1)
        conf=1.96*conf/math.sqrt(len(self.times))
        ret.append([T,conf])

        #W and interval calculation
        conf=0
        W=self.W/self.counterTime
        for i in self.times:
            conf+=(i[2]-W)**2
        conf/=(len(self.times)-1)
        conf=1.96*conf/math.sqrt(len(self.times))
        ret.append([W,conf])

        #X_r and interval calculation
        conf=0
        X_r=(self.X_2/self.counterTime)/(2*(self.X/self.counterTime))
        for i in self.times:
            conf+=(i[3]/(2*i[0])-X_r)**2
        conf/=(len(self.times)-1)
        conf=1.96*conf/math.sqrt(len(self.times))
        ret.append([X_r,conf])

        #N_q1 and interval calculation
        conf=0
        N_q1=self.N_q1/self.lastT
        for i in self.allQueues:
            counter=0
            for j in i[3]:
                if j[0]==1:
                    counter+=1
            conf+=(counter-N_q1)**2
        conf/=(len(self.allQueues)-1)
        conf=1.96*conf/math.sqrt(len(self.allQueues))
        ret.append([N_q1,conf])

        #N_q2 and interval calculation
        conf=0
        N_q2=self.N_q2/self.lastT
        for i in self.allQueues:
            counter=0
            for j in i[3]:
                if j[0]==2:
                    counter+=1
            conf+=(counter-N_q2)**2
        conf/=(len(self.allQueues)-1)
        conf=1.96*conf/math.sqrt(len(self.allQueues))
        ret.append([N_q2,conf])

        #X_1 and interval calculation
        conf=0
        X_1=self.X_1/self.counterTime
        for i in self.times1:
            conf+=(i[0]-X_1)**2
        conf/=(len(self.times1)-1)
        conf=1.96*conf/math.sqrt(len(self.times1))
        ret.append([X_1,conf])

        #T_1 and interval calculation
        conf=0
        T_1=self.T_1/self.counterTime
        for i in self.times1:
            conf+=(i[1]-T_1)**2
        conf/=(len(self.times1)-1)
        conf=1.96*conf/math.sqrt(len(self.times1))
        ret.append([T_1,conf])

        #W_1 and interval calculation
        conf=0
        W_1=self.W_1/self.counterTime
        for i in self.times1:
            conf+=(i[2]-W_1)**2
        conf/=(len(self.times1)-1)
        conf=1.96*conf/math.sqrt(len(self.times1))
        ret.append([W_1,conf])

        #X_r1 and interval calculation
        conf=0
        X_r1=(self.X_1_2/self.counterTime)/(2*(self.X_1/self.counterTime))
        for i in self.times1:
            conf+=(i[3]/(2*i[0])-X_r1)**2
        conf/=(len(self.times1)-1)
        conf=1.96*conf/math.sqrt(len(self.times1))
        ret.append([X_r1,conf])

        #X_2 and interval calculation
        conf=0
        X_2=self.X_2/self.counterTime
        for i in self.times2:
            conf+=(i[0]-X_2)**2
        conf/=(len(self.times2)-1)
        conf=1.96*conf/math.sqrt(len(self.times2))
        ret.append([X_2,conf])

        #T_2 and interval calculation
        conf=0
        T_2=self.T_2/self.counterTime
        for i in self.times2:
            conf+=(i[1]-T_2)**2
        conf/=(len(self.times2)-1)
        conf=1.96*conf/math.sqrt(len(self.times2))
        ret.append([T_2,conf])

        #W_2 and interval calculation
        conf=0
        W_2=self.W_2/self.counterTime
        for i in self.times2:
            conf+=(i[2]-W_2)**2
        conf/=(len(self.times2)-1)
        conf=1.96*conf/math.sqrt(len(self.times2))
        ret.append([W_2,conf])

        #X_r2 and interval calculation
        conf=0
        X_r2=(self.X_2_2/self.counterTime)/(2*(self.X_2/self.counterTime))
        for i in self.times2:
            conf+=(i[3]/(2*i[0])-X_r2)**2
        conf/=(len(self.times2)-1)
        conf=1.96*conf/math.sqrt(len(self.times2))
        ret.append([X_r2,conf])

        #return [
        #[N_q , Err] , [N_s , Err] , [N , Err] , [X , Err] , [T , Err] ,
        #[W , Err] , [X_r , err] , [N_q1 , err] [N_q1 , err] ,
        #[X_1 , err] , [T_1 , err] , [W_1 , err] , [X_r1 , err],
        #[X_2 , err] , [T_2 , err] , [W_2 , err] , [X_r2 , err]
        #]
        return ret

    #function that  reinicialize the queue
    def reinitQueue(self):
        self.__Init__()


#MAIN
#queue data struct [ [T], [Class_in0 , I_in0,T_in0] , [Class_in1 , I_in1,T_in1] , [ [Class_waith1,I_wait1,T_wait1] , [Class_waith1,I_wait2,T_wait2] ,... ] , [out1,out2,out3,out4] ]
if __name__ == "__main__":

    #list to store the queue and waits
    queue=[]
    wait=[]

    parameters=CalculateParameters()

    inputFile=open('fila','r')

    lines=inputFile.readlines()
    for i in lines:
        waitTmp=[]
        time=[]
        IN=[]
        out=[]
        splited=i.split(' ')

        if splited[0]=='T:':
            time.append(float(splited[1]))
            queue.append(time)

        elif splited[0]=='IN_0:' or splited[0]=='IN_0:\n':
            if len(splited)>1:
                splited2=[]
                splited2=splited[1].split('|')
                IN.append(int(splited2[1]))
                IN.append(float(splited2[2]))
                IN.append(float(splited2[3]))
            queue.append(IN)

        elif splited[0]=='IN_1:' or splited[0]=='IN_1:\n':
            if len(splited)>1:
                splited2=[]
                splited2=splited[1].split('|')
                IN.append(int(splited2[1]))
                IN.append(float(splited2[2]))
                IN.append(float(splited2[3]))
            queue.append(IN)

        elif splited[0]=='WAIT_0:' or splited[0]=='WAIT_0:\n':
            if len(splited)>1:
                splited2=[]
                splited2=splited[1].split('|')
                waitTmp.append(int(splited2[1]))
                waitTmp.append(float(splited2[2]))
                waitTmp.append(float(splited2[3]))
                wait.append(waitTmp)
                waitTmp=[]

        elif splited[0]=='OUT_0:' or splited[0]=='OUT_0:\n':
            if len(splited)>1:
                splited2=[]
                splited2=splited[1].split('|')
                out.append(int(splited2[1]))
                out.append(float(splited2[2]))
                out.append(float(splited2[3]))
                out.append(float(splited2[4]))
                out.append(float(splited2[5]))
            queue.append(wait)
            queue.append(out)
            #queue pronto trabalhar a partir daqui
            #print(queue)
            parameters.updateQueue(queue)
            wait=[]
            queue=[]

    inputFile.close()
    result=parameters.returnResults()
    print ('E[N]=%f +- %f\n' %(result[2][0] ,result[2][1]))
    print ('E[N_q]=%f +- %f\n' %(result[0][0] ,result[0][1]))
    print ('E[N_s]=%f +- %f\n' %(result[1][0] ,result[1][1]))
    print ('E[X]=%f +- %f\n' %(result[3][0] ,result[3][1]))
    print ('E[T]=%f +- %f\n' %(result[4][0] ,result[4][1]))
    print ('E[W]=%f +- %f\n' %(result[5][0] ,result[5][1]))
    print ('E[X_r]=%f +- %f\n' %(result[6][0] ,result[6][1]))
    print ('E[N_q1]=%f +- %f\n' %(result[7][0] ,result[7][1]))
    print ('E[N_q2]=%f +- %f\n' %(result[8][0] ,result[8][1]))

    print ('E[X_1]=%f +- %f\n' %(result[9][0] ,result[9][1]))
    print ('E[T_1]=%f +- %f\n' %(result[10][0] ,result[10][1]))
    print ('E[W_1]=%f +- %f\n' %(result[11][0] ,result[11][1]))
    print ('E[X_r1]=%f +- %f\n' %(result[12][0] ,result[12][1]))

    print ('E[X_2]=%f +- %f\n' %(result[13][0] ,result[13][1]))
    print ('E[T_2]=%f +- %f\n' %(result[14][0] ,result[14][1]))
    print ('E[W_2]=%f +- %f\n' %(result[15][0] ,result[15][1]))
    print ('E[X_r2]=%f +- %f\n' %(result[16][0] ,result[16][1]))
    print("\n")
    print(result)
