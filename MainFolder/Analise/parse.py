class Parse:
    def __init__(self,fileIN='fila'):
        self.fileName=fileIN

    def parseDo(self):
        queue=[]
        wait=[]
        retQueue=[]

        inputFile=open(self.fileName,'r')

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
                    if(splited2[1]=='None'):
                        IN.append(-1)
                    else:
                        IN.append(float(splited2[1]))
                    IN.append(float(splited2[2]))
                    IN.append(float(splited2[3]))
                    IN.append(float(splited2[4]))
                    IN.append(float(splited2[5]))
                    IN.append(float(splited2[6]))
                queue.append(IN)

            elif splited[0]=='IN_1:' or splited[0]=='IN_1:\n':
                if len(splited)>1:
                    splited2=[]
                    splited2=splited[1].split('|')
                    if(splited2[1]=='None'):
                        IN.append(-1)
                    else:
                        IN.append(float(splited2[1]))
                    IN.append(float(splited2[2]))
                    IN.append(float(splited2[3]))
                    IN.append(float(splited2[4]))
                    IN.append(float(splited2[5]))
                    IN.append(float(splited2[6]))
                queue.append(IN)

            elif splited[0]=='WAIT_0:' or splited[0]=='WAIT_0:\n':
                if len(splited)>1:
                    splited2=[]
                    splited2=splited[1].split('|')
                    if(splited2[1]=='None'):
                        waitTmp.append(-1)
                    else:
                        waitTmp.append(float(splited2[1]))
                    waitTmp.append(float(splited2[2]))
                    waitTmp.append(float(splited2[3]))
                    waitTmp.append(float(splited2[4]))
                    waitTmp.append(float(splited2[5]))
                    waitTmp.append(float(splited2[6]))
                    wait.append(waitTmp)
                    waitTmp=[]

            elif splited[0]=='OUT_0:' or splited[0]=='OUT_0:\n':
                if len(splited)>1:
                    splited2=[]
                    splited2=splited[1].split('|')
                    if(splited2[1]=='None'):
                        out.append(-1)
                    else:
                        out.append(float(splited2[1]))
                    out.append(float(splited2[2]))
                    out.append(float(splited2[3]))
                    out.append(float(splited2[4]))
                    out.append(float(splited2[5]))
                    out.append(float(splited2[6]))
                queue.append(wait)
                queue.append(out)
                wait=[]
                retQueue.append(queue)
                queue=[]

        inputFile.close()
        return retQueue

    '''return of parseDo(self) function:
    [
        [
            [T1],[Class_IN1],[Indice_IN1],[Chegada_IN1],[Trabalho_IN1],[Saída_IN1],[Última_IN1]
        ],
        [

        ],
        .
        .
        .
    ]'''
