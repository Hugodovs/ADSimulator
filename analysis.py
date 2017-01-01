#class that receive states of a queue and calculate individualy usefull quantities
#like /ro, E[U], E[X_r]...
class CalculateParameters:
    def __Init__(self):
        self.N=0
        self.N_q=0
        self.N_s=0
        self.T=0
        self.X=0
        self.U=0
        self.X_r=0
        self.counter=0

    #function that receive a new state of queue and update the parameters
    def updateQueue(self,queue):
        pass

    #function that return the final values calculated
    def returnResults(self):
        return [1,2,3]

    #function that  reinicialize the queue
    def reinitQueue(self):
        self.__Init__()

        
#MAIN
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
            
        elif splited[0]=='IN_0:':
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
            wait=[]
            queue=[]

    inputFile.close()
    result=parameters.returnResults()
    print(result)
    
