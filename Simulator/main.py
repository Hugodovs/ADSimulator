from bubble import *

if __name__ == "__main__":
    
    np.random.seed(105)
    
    bank = System("bank")
    bank.create_IN_Bubble(typePerson = "1")
    bank.create_IN_Bubble(typePerson = "2")
    bank.create_WAIT_Bubble(policy="FCFS", preemption=True, priority=[1,2])
    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
    bank.connect("IN_Bubble", 1, "WAIT_Bubble", 0)
    bank.create_OUT_Bubble()
    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)
    bank.startSystem()
    bank.printSystemState()
    
    for i in range(10):
        bank.run_episode(printstates = True)
    
#===============================#
#1) FCFS sem distinção de classes (fila única)

####    np.random.seed(105)
####    
####    bank = System("bank")
####    bank.create_IN_Bubble()
####    bank.create_WAIT_Bubble(policy="FCFS")
####    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
####    bank.create_OUT_Bubble()
####    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)
####    bank.startSystem()
####    bank.printSystemState()
####    
####    for i in range(10):
####        bank.run_episode(printstates = True)

#===============================#
#2) LCFS sem preempção sem distinção de classes (fila única)

####    np.random.seed(105)
####    
####    bank = System("bank")
####    bank.create_IN_Bubble()
####    bank.create_WAIT_Bubble(policy="LCFS")
####    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
####    bank.create_OUT_Bubble()
####    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)
####    bank.startSystem()
####    bank.printSystemState()
####    
####    for i in range(10):
####        bank.run_episode(printstates = True)

#===============================#
#3) LCFS com preempção e sem distinção de classes (fila única)

####    np.random.seed(105)
####    
####    bank = System("bank")
####    bank.create_IN_Bubble()
####    bank.create_WAIT_Bubble(policy="FCFS", preemption=True)
####    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
####    bank.create_OUT_Bubble()
####    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)
####    bank.startSystem()
####    bank.printSystemState()
####    
####    for i in range(10):
####        bank.run_episode(printstates = True)

#===============================#
#4) FCFS sem preempção e com classe 1 com prioridade sobre classe 2 (fila única)

####np.random.seed(105)
####    
####    bank = System("bank")
####    bank.create_IN_Bubble(typePerson = "1")
####    bank.create_IN_Bubble(typePerson = "2")
####    bank.create_WAIT_Bubble(policy="FCFS", preemption=True, priority=[1,2])
####    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
####    bank.connect("IN_Bubble", 1, "WAIT_Bubble", 0)
####    bank.create_OUT_Bubble()
####    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)
####    bank.startSystem()
####    bank.printSystemState()
####    
####    for i in range(10):
####        bank.run_episode(printstates = True)







