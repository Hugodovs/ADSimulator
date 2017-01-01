#class that receive states of a queue and calculate individualy usefull quantities
#like /ro, E[U], E[X_r]...
class CalculateParameters:
    def __init__(self):
        #self.N=0
        self.N_q=0
        self.N_s=0
        self.T=0
        self.X=0
        self.U=0
        self.X_r=0
        self.counter=0
        self.lastT=0

    #function that receive a new state of queue and update the parameters
    def updateQueue(self,queue):
        #calculate N_q and N_s only if T differs from 0
        if self.counter!=0:
            self.N_q+=len(queue[2])*(queue[0][0]-self.lastT)
            if len(queue[3])>0:
                self.N_s+=(queue[0][0]-self.lastT)

        #calculate T, X and W
        
            
        self.counter+=1
        self.lastT=queue[0][0]

    #function that return the final values calculated
    def returnResults(self):
        if self.counter==0:
            return []
        
        ret=[]
        ret.append((self.N_q+self.N_s)/self.lastT)
        ret.append(self.N_q/self.lastT)
        ret.append(self.N_s/self.lastT)

        return ret

    #function that  reinicialize the queue
    def reinitQueue(self):
        self.__Init__()

        
#MAIN
#queue data struct [ [T], [I_in,T_in] , [ [I_wait1,T_wait1] , [I_wait2,T_wait2] ,... ] , [out1,out2,out3] ]
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
            time.append(int(splited[1]))
            queue.append(time)
            
        elif splited[0]=='IN_0:' or splited[0]=='IN_0:\n':
            if len(splited)>1:
                splited2=splited[1].split('|')
                IN.append(int(splited2[1]))
                IN.append(int(splited2[2]))
            queue.append(IN)
            
        elif splited[0]=='WAIT_0:' or splited[0]=='WAIT_0:\n':
            if len(splited)>1:
                plited2=splited[1].split('|')
                waitTmp.append(int(splited2[1]))
                waitTmp.append(int(splited2[2]))
                wait.append(waitTmp)
                
        elif splited[0]=='OUT_0:' or splited[0]=='OUT_0:\n':
            if len(splited)>1:
                splited2=splited[1].split('|')
                out.append(int(splited2[1]))
                out.append(int(splited2[2]))
                out.append(int(splited2[3]))
                out.append(int(splited2[4]))
            queue.append(wait)
            queue.append(out)
            parameters.updateQueue(queue)
            print(queue)
            wait=[]
            queue=[]

    inputFile.close()
    result=parameters.returnResults()
    print(result)
    
