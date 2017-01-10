import Simulator.bubble as bb
import numpy as np

def returnVectorNumerical():
    #MAIN
    return points_vector

def runQueue(i):
    np.random.seed(i)
        
    bank = bb.System("bank")
    bank.create_IN_Bubble()
    bank.create_WAIT_Bubble(policy="FCFS")
    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
    bank.create_OUT_Bubble()
    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)
    bank.startSystem()
    finalString = bank.saveInString()
        
    for i in range(2000):
        finalString += bank.run_episode(printstates = True)
    
    with open("arquivo.txt", "w") as f:
        f.write(finalString)
        
    return finalString

if __name__ == "__main__":
        
    for i in range(100):
        
        finalString = runQueue(i)
        
        #Do whatever you want with finalString
        #...
        
        
        
        
        
        
