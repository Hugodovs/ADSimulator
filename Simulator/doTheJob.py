def doTheJob(lambda_init=1,lambda_end=10,lambda_step=1,mi_init=1,mi_end=10,mi_step=1,politics=1):
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
                if(mi>lambda):
                    #generate the queues for analysis
                    bank.create_IN_Bubble()
                    bank.create_WAIT_Bubble(policy="FCFS")
                    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
                    bank.create_OUT_Bubble()
                    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)

                    bank.startSystem()
                    bank.printSystemState()

                    for i in range(10000):
                        bank.run_episode(printstates = True)

                    #analysis of file
                    queue=parse.parseDo()
                    for i in queue:
                        parameters.updateQueue(i)
                    result=parameters.returnResults()

                    #generate array for print
                    lambda_par.append(i)
                    mi_par.append(j)

    elif(politics==2):


    elif(politics==3):


    elif(politics==4);


    elif(politics==5):
