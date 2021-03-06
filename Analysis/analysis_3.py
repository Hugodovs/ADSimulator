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
        self.personsPre=[]

    #function that receive a new state of queue and update the parameters
    def updateQueue(self,queue):
        #calculate N_q and N_s only if T differs from 0
        if self.counter!=0:
            self.N_q+=len(queue[2])*(queue[0][0]-self.lastT)
            if len(queue[3])>0:
                self.N_s+=(queue[0][0]-self.lastT)

        #calculate T, X and W and X_r
        if len(queue[3])>0 and queue[3][0]!=self.lastOut:
            self.X_2+=(queue[3][2])**2
            self.X+=queue[3][2]
            self.T+=queue[3][3]-queue[3][1]
            self.W+=queue[3][3]-queue[3][1]-queue[3][2]
            for i in self.personsPre:
                if(queue[3][0]==i[0]):
                    self.X+=i[1]
                    self.T+=i[2]
                    self.W+=i[3]
                    self.X_2+=i[4]
            self.times.append([queue[3][2],queue[3][3]-queue[3][1],queue[3][3]-queue[3][1]-queue[3][2],(queue[3][2])**2])
            for i in range(0,len(self.personsPre)):
                if(queue[3][0]==self.personsPre[i][0]):
                    personsPre[i][1]=self.X
                    personsPre[i][2]=self.T
                    personsPre[i][3]=self.W
                    personsPre[i][4]=self.X_2
                else:
                    self.personsPre.append([queue[3][0],queue[3][2],queue[3][3]-queue[3][1],queue[3][3]-queue[3][1]-queue[3][2],(queue[3][2])**2])

            self.lastOut=queue[3][0]
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
            conf+=(len(i[2])-N_q)**2
        conf/=(len(self.allQueues)-1)
        conf=1.96*conf/math.sqrt(len(self.allQueues))
        ret.append([N_q,conf])

        #N_s and interval calculation
        conf=0
        N_s=self.N_s/self.lastT
        for i in self.allQueues:
            if(len(i[3])>0):
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
            if(len(i[3])>0):
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


        #return [ [N_q , Err] , [N_s , Err] , [N , Err] , [X , Err] , [T , Err] , [W , Err] , [X_r , err]]
        return ret

    #function that  reinicialize the queue
    def reinitQueue(self):
        self.__Init__()


#MAIN
#queue data struct [ [T], [I_in,T_in] , [ [I_wait1,T_wait1] , [I_wait2,T_wait2] ,... ] , [out1,out2,out3,out4] ]
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
                IN.append(float(splited2[1]))
                IN.append(float(splited2[2]))
            queue.append(IN)

        elif splited[0]=='WAIT_0:' or splited[0]=='WAIT_0:\n':
            if len(splited)>1:
                splited2=[]
                splited2=splited[1].split('|')
                waitTmp.append(float(splited2[1]))
                waitTmp.append(float(splited2[2]))
                wait.append(waitTmp)
                waitTmp=[]

        elif splited[0]=='OUT_0:' or splited[0]=='OUT_0:\n':
            if len(splited)>1:
                splited2=[]
                splited2=splited[1].split('|')
                out.append(float(splited2[1]))
                out.append(float(splited2[2]))
                out.append(float(splited2[3]))
                out.append(float(splited2[4]))
            queue.append(wait)
            queue.append(out)
            #queue pronto trabalhar a partir daqui
            print(queue)
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
    print("\n")
    print(result)

    def Analisys():

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
                    splited2=splited[1].split('|')
                    IN.append(float(splited2[1]))
                    IN.append(float(splited2[2]))
                queue.append(IN)

            elif splited[0]=='WAIT_0:' or splited[0]=='WAIT_0:\n':
                if len(splited)>1:
                    plited2=splited[1].split('|')
                    waitTmp.append(float(splited2[1]))
                    waitTmp.append(float(splited2[2]))
                    wait.append(waitTmp)

            elif splited[0]=='OUT_0:' or splited[0]=='OUT_0:\n':
                if len(splited)>1:
                    splited2=splited[1].split('|')
                    out.append(float(splited2[1]))
                    out.append(float(splited2[2]))
                    out.append(float(splited2[3]))
                    out.append(float(splited2[4]))
                queue.append(wait)
                queue.append(out)
                #queue pronto trabalhar a partir daqui
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
        print("\n")
        print(result)

        return result
