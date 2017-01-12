import math

#class that receive states of a queue and calculate individualy usefull quantities
#like /ro, E[U], E[X_r]...
class CalculateParameters:
    def __init__(self):
        #self.N=0
        self.N_q=0
        self.N_q_array=[]
        self.N_s=0
        self.N_s_array=[]
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
        self.N_q1_array=[]
        self.N_q2_array=[]
        self.N_array=[]

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
        self.W_1_array=[]
        self.W_2_array=[]
        self.W_array=[]

        self.T_1_array=[]
        self.T_2_array=[]
        self.T_array=[]

        self.X_1_array=[]
        self.X_2_array=[]
        self.X_array=[]

        self.X_r_1_array=[]
        self.X_r_2_array=[]
        self.X_r_array=[]

        self.X_quad=0

        self.B=0
        self.B_array=[]

        self.U_array=[]

        '''array to store preempted persons
        [
        [class, index, T, W],
        [class2, index2, T2, W2]
        ]'''
        self.preemp=[]

    #function that receive a new state of queue and update the parameters
    def updateQueue(self,queue):
        if (self.counter==0):
            #analysis of queue struct
            if(len(queue)==5):
                self.T_index=0
                self.IN_0_index=1
                self.IN_1_index=2
                self.WAIT_0_index=3
                self.OUT_0_index=4
            elif(len(queue)==4):
                self.T_index=0
                self.IN_0_index=1
                self.IN_1_index=1
                self.WAIT_0_index=2
                self.OUT_0_index=3
            #indexes of persons parameters
            self.time_index=0
            self.class_index=0
            self.index_index=1
            self.come_index=2
            self.work_index=3
            self.out_index=4
            self.last_index=5
        #calculate N_q and N_s only if T differs from 0
        if self.counter!=0 :
            self.N_q+=len(queue[self.WAIT_0_index])*(queue[self.T_index][self.time_index]-self.lastT)
            self.N_q_array.append(self.N_q/queue[self.T_index][self.time_index])

            counter1=0
            counter2=0
            for q1 in queue[self.WAIT_0_index]:
                if q1[self.class_index]==1:
                    counter1+=1
                elif q1[self.class_index]==2:
                    counter2+=1
                else:
                    counter1+=1
                    counter2+=1
            self.N_q1+=counter1*(queue[self.T_index][self.time_index]-self.lastT)
            self.N_q2+=counter2*(queue[self.T_index][self.time_index]-self.lastT)
            self.N_q1_array.append(self.N_q1/queue[self.T_index][self.time_index])
            self.N_q2_array.append(self.N_q2/queue[self.T_index][self.time_index])
            if len(queue[self.OUT_0_index])>0:
                self.N_s+=(queue[self.T_index][self.time_index]-self.lastT)
                self.N_s_array.append(self.N_s/queue[self.T_index][self.time_index])
            else:
                self.N_s_array.append(0)
            self.N_array.append((self.N_q+self.N_s)/queue[self.T_index][self.time_index])

        #calculate T, X and W and X_r
        if (len(queue[self.OUT_0_index])>0 and queue[self.OUT_0_index][self.index_index]!=self.lastOut):

            preempted=False
            for i in self.preemp:
                if (i[1]==queue[self.OUT_0_index][self.index_index]):
                    preempted=True
                    break

            if (preempted==False):
                self.X_quad+=(queue[self.OUT_0_index][self.work_index])**2
                self.X+=queue[self.OUT_0_index][self.work_index]
                self.T+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]
                self.W+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index]
                self.times.append([queue[self.OUT_0_index][self.work_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index],(queue[self.OUT_0_index][self.work_index])**2])
                self.X_array.append(self.X/(self.counterTime+1))
                self.B+=queue[self.OUT_0_index][self.work_index]
                self.B_array.append(self.B/queue[0][0])

            else:
                self.T+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]
                self.W+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]-queue[self.OUT_0_index][self.work_index]
            self.T_array.append(self.T/(self.counterTime+1))
            self.W_array.append(self.W/(self.counterTime+1))
            tmp=(self.X/(self.counterTime+1))**2/(2*self.X/(self.counterTime+1))
            self.X_r_array.append(tmp)

            if (queue[self.OUT_0_index][self.class_index]==1):
                if(preempted==False):
                    self.X_1_2+=(queue[self.OUT_0_index][self.work_index])**2
                    self.X_1+=queue[self.OUT_0_index][self.work_index]
                    self.T_1+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]
                    self.W_1+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index]
                    self.times1.append([queue[self.OUT_0_index][self.work_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index],(queue[self.OUT_0_index][self.work_index])**2])
                    self.counterTime1+=1
                    self.X_1_array.append(self.X_1/(self.counterTime1))

                else:
                    self.T_1+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]
                    self.W_1+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]-queue[self.OUT_0_index][self.work_index]
                    self.counterTime1+=1

                self.T_1_array.append(self.T_1/(self.counterTime1))
                self.W_1_array.append(self.W_1/(self.counterTime1))
                tmp=(self.X_1_2/self.counterTime1)/(2*self.X_1/(self.counterTime1))
                self.X_r_1_array.append(tmp)

            elif(queue[self.OUT_0_index][self.class_index]==2):
                if(preempted==False):
                    self.X_2_2+=(queue[self.OUT_0_index][self.work_index])**2
                    self.X_2+=queue[self.OUT_0_index][self.work_index]
                    self.T_2+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]
                    self.W_2+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index]
                    self.times2.append([queue[self.OUT_0_index][self.work_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index],(queue[self.OUT_0_index][self.work_index])**2])
                    self.counterTime2+=1
                    self.X_2_array.append(self.X_2/(self.counterTime2))

                else:
                    self.T_2+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]
                    self.W_2+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]-queue[self.OUT_0_index][self.work_index]
                    self.counterTime2+=1

                self.T_2_array.append(self.T_2/(self.counterTime2))
                self.W_2_array.append(self.W_2/(self.counterTime2))
                tmp=(self.X_2_2/self.counterTime2)/(2*self.X_2/(self.counterTime2))
                self.X_r_2_array.append(tmp)

            else:
                if(preempted==False):
                    self.X_1_2+=(queue[self.OUT_0_index][self.work_index])**2
                    self.X_1+=queue[self.OUT_0_index][self.work_index]
                    self.T_1+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]
                    self.W_1+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index]
                    self.times1.append([queue[self.OUT_0_index][self.work_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index],(queue[self.OUT_0_index][self.work_index])**2])
                    self.counterTime1+=1
                    self.X_1_array.append(self.X_1/(self.counterTime1))

                else:
                    self.T_1+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]
                    self.W_1+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]-queue[self.OUT_0_index][self.work_index]
                    self.counterTime1+=1

                self.T_1_array.append(self.T_1/(self.counterTime1))
                self.W_1_array.append(self.W_1/(self.counterTime1))
                tmp=(self.X_1_2/self.counterTime1)/(2*self.X_1/(self.counterTime1))
                self.X_r_1_array.append(tmp)

                if(preempted==False):
                    self.X_2_2+=(queue[self.OUT_0_index][self.work_index])**2
                    self.X_2+=queue[self.OUT_0_index][self.work_index]
                    self.T_2+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]
                    self.W_2+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index]
                    self.times2.append([queue[self.OUT_0_index][self.work_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index],queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.come_index]-queue[self.OUT_0_index][self.work_index],(queue[self.OUT_0_index][self.work_index])**2])
                    self.counterTime2+=1
                    self.X_2_array.append(self.X_2/(self.counterTime2))

                else:
                    self.T_2+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]
                    self.W_2+=queue[self.OUT_0_index][self.out_index]-queue[self.OUT_0_index][self.last_index]-queue[self.OUT_0_index][self.work_index]
                    self.counterTime2+=1

                self.T_2_array.append(self.T_2/(self.counterTime2))
                self.W_2_array.append(self.W_2/(self.counterTime2))
                tmp=(self.X_2_2/self.counterTime2)/(2*self.X_2/(self.counterTime2))
                self.X_r_2_array.append(tmp)



            self.lastOut=queue[self.OUT_0_index][self.index_index]
            self.counterTime+=1
            if(self.lastT!=0 and self.counterTime!=0 and self.W and self.X):
                ro_tmp=(self.N_q/(self.lastT))*(self.X/self.counterTime)/(self.W/self.counterTime)
                self.U_array.append(ro_tmp*((self.X/self.counterTime)**2/(2*(self.X/self.counterTime)))/(1-ro_tmp))

        self.counter+=1
        self.lastT=queue[self.T_index][self.time_index]
        self.allQueues.append(queue)

    #function that return the final values calculated
    def returnResults(self):
        if self.counter==0:
            return []

        ret=[]

        #N_q and interval calculation
        conf=0
        N_q=self.N_q/self.lastT
        for i in self.N_q_array:
            conf+=(i-N_q)**2
        conf/=(len(self.N_q_array)-1)
        conf=1.96*conf/math.sqrt(len(self.N_q_array))
        ret.append([N_q,conf])

        #N_s and interval calculation
        conf=0
        N_s=self.N_s/self.lastT
        for i in self.N_s_array:
            conf+=(i-N_s)**2
        conf/=(len(self.N_s_array)-1)
        conf=1.96*conf/math.sqrt(len(self.N_s_array))
        ret.append([N_s,conf])

        #N and interval calculation
        conf=0
        N=(self.N_q+self.N_s)/self.lastT
        for i in self.N_array:
            conf+=(i-N)**2
        conf/=(len(self.N_array)-1)
        conf=1.96*conf/math.sqrt(len(self.N_array))
        ret.append([N,conf])

        #X and interval calculation
        conf=0
        X=self.X/self.counterTime
        for i in self.X_array:
            conf+=(i-X)**2
        conf/=(len(self.X_array)-1)
        conf=1.96*conf/math.sqrt(len(self.X_array))
        ret.append([X,conf])

        #T and interval calculation
        conf=0
        T=self.T/self.counterTime
        for i in self.T_array:
            conf+=(i-T)**2
        conf/=(len(self.T_array)-1)
        conf=1.96*conf/math.sqrt(len(self.T_array))
        ret.append([T,conf])

        #W and interval calculation
        conf=0
        W=self.W/self.counterTime
        for i in self.W_array:
            conf+=(i-W)**2
        conf/=(len(self.W_array)-1)
        conf=1.96*conf/math.sqrt(len(self.W_array))
        ret.append([W,conf])

        #X_r and interval calculation
        conf=0
        X_r=(self.X/self.counterTime)**2/(2*(self.X/self.counterTime))
        for i in self.X_r_array:
            conf+=(i-X_r)**2
        conf/=(len(self.X_r_array)-1)
        conf=1.96*conf/math.sqrt(len(self.X_r_array))
        ret.append([X_r,conf])

        #N_q1 and interval calculation
        conf=0
        N_q1=self.N_q1/self.lastT
        for i in self.N_q1_array:
            conf+=(i-N_q1)**2
        conf/=(len(self.N_q1_array)-1)
        conf=1.96*conf/math.sqrt(len(self.N_q1_array))
        ret.append([N_q1,conf])

        #N_q2 and interval calculation
        conf=0
        N_q2=self.N_q2/self.lastT
        for i in self.N_q2_array:
            conf+=(i-N_q2)**2
        conf/=(len(self.N_q2_array)-1)
        conf=1.96*conf/math.sqrt(len(self.N_q2_array))
        ret.append([N_q2,conf])

        #X_1 and interval calculation
        conf=0
        X_1=self.X_1/self.counterTime
        for i in self.X_1_array:
            conf+=(i-X_1)**2
        conf/=(len(self.X_1_array)-1)
        conf=1.96*conf/math.sqrt(len(self.X_1_array))
        ret.append([X_1,conf])

        #T_1 and interval calculation
        conf=0
        T_1=self.T_1/self.counterTime
        for i in self.T_1_array:
            conf+=(i-T_1)**2
        conf/=(len(self.T_1_array)-1)
        conf=1.96*conf/math.sqrt(len(self.T_1_array))
        ret.append([T_1,conf])

        #W_1 and interval calculation
        conf=0
        W_1=self.W_1/self.counterTime
        for i in self.W_1_array:
            conf+=(i-W_1)**2
        conf/=(len(self.W_1_array)-1)
        conf=1.96*conf/math.sqrt(len(self.W_1_array))
        ret.append([W_1,conf])

        #X_r1 and interval calculation
        conf=0
        X_r1=(self.X_1_2/self.counterTime)/(2*(self.X_1/self.counterTime))
        for i in self.X_r_1_array:
            conf+=(i-X_r1)**2
        conf/=(len(self.X_r_1_array)-1)
        conf=1.96*conf/math.sqrt(len(self.X_r_1_array))
        ret.append([X_r1,conf])

        #X_2 and interval calculation
        conf=0
        X_2=self.X_2/self.counterTime
        for i in self.X_2_array:
            conf+=(i-X_2)**2
        conf/=(len(self.X_2_array)-1)
        conf=1.96*conf/math.sqrt(len(self.X_2_array))
        ret.append([X_2,conf])

        #T_2 and interval calculation
        conf=0
        T_2=self.T_2/self.counterTime
        for i in self.T_2_array:
            conf+=(i-T_2)**2
        conf/=(len(self.T_2_array)-1)
        conf=1.96*conf/math.sqrt(len(self.T_2_array))
        ret.append([T_2,conf])

        #W_2 and interval calculation
        conf=0
        W_2=self.W_2/self.counterTime
        for i in self.W_2_array:
            conf+=(i-W_2)**2
        conf/=(len(self.W_2_array)-1)
        conf=1.96*conf/math.sqrt(len(self.W_2_array))
        ret.append([W_2,conf])

        #X_r2 and interval calculation
        conf=0
        X_r2=(self.X_2_2/self.counterTime)/(2*(self.X_2/self.counterTime))
        for i in self.X_r_2_array:
            conf+=(i-X_r2)**2
        conf/=(len(self.X_r_2_array)-1)
        conf=1.96*conf/math.sqrt(len(self.X_r_2_array))
        ret.append([X_r2,conf])

        #B and interval calculation
        conf=0
        B=self.B/self.lastT
        for i in self.B_array:
            conf+=(i-B)**2
        conf/=(len(self.B_array)-1)
        conf=1.96*conf/math.sqrt(len(self.B_array))
        ret.append([B,conf])

        #U and interval calculation
        conf=0
        ro_tmp=N_q*X/W
        U=ro_tmp*X_r/(2*(1-ro_tmp))
        for i in self.U_array:
            conf+=(i-U)**2
        conf/=(len(self.U_array)-1)
        conf=1.96*conf/math.sqrt(len(self.U_array))
        ret.append([U,conf])

        #return [
        #[N_q , Err] , [N_s , Err] , [N , Err] , [X , Err] , [T , Err] ,
        #[W , Err] , [X_r , err] , [N_q1 , err] [N_q1 , err] ,
        #[X_1 , err] , [T_1 , err] , [W_1 , err] , [X_r1 , err],
        #[X_2 , err] , [T_2 , err] , [W_2 , err] , [X_r2 , err]
        #]
        return ret

    #function that  reinicialize the queue
    def reinitQueue(self):
        self.__init__()
