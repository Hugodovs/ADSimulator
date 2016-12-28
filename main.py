#Author: Hugo Siqueira Gomes
#Project: Three-Bubble-System

#Who can connect:
# IN_Bubble:
#   entrance_connector:    
#   exit_connectors: WAIT_Bubble, OUT_Bubble
#     
# WAIT_Bubble:
#   entrance_connector: IN_Bubble, OUT_Bubble   
#   exit_connectors: OUT_Bubble
#     
# OUT_Bubble:
#   entrance_connector: IN_Bubble, WAIT_Bubble 
#   exit_connectors: WAIT_Bubble, OUT_Bubble
#     

#==========================================================================

import numpy as np

#=============== OBJECTS FOR THE SYSTEM ===================================
class IN_Bubble:
    def __init__(self, rate = 5, typeRate = "Poisson", start = 0): 
        self.rate = rate
        self.typeRate = typeRate
        self.start = start
        self.nextPerson = None
        
        self.nextEvent = -1
        self.exit_connectors = []
                
    def receivePerson(self, index, actualClock):
        if self.typeRate == "Poisson":
            arrivalTime = actualClock + np.random.poisson(self.rate)
        newPerson = Person(index, arrivalTime)

        self.nextPerson = newPerson
        self.nextEvent = arrivalTime
        return True
        
    def sendPerson(self):
        index = np.random.randint(len(self.exit_connectors))
        self.exit_connectors[index].receivePerson(self.nextPerson)
        self.nextPerson = None

    def connect_WAIT(self, WAIT_Bubble):
        self.exit_connectors.append(WAIT_Bubble)

    def connect_OUT(self, OUT_Bubble):
        self.exit_connectors.append(OUT_Bubble)
        
class WAIT_Bubble:
    def __init__(self, policy = "FIFO"):
        self.peopleList = []
        
        self.exit_connectors = []
        
    def receivePerson(self, person):
        status = self.try_OUT(person)
        if status == True:
            return
            
        self.peopleList.append(person)
        return
        
    def try_OUT(self, person):
        for item in self.exit_connectors:
            status = item.receivePerson(person)  
            if status == True:
                return True
        return False
                
    def sendPerson(self, person):
        pass
        
    def connect_OUT(self, OUT_Bubble):
        self.exit_connectors.append(OUT_Bubble)    
        
class OUT_Bubble:
    def __init__(self, rate = 5, typeRate = "Poisson", start = 0):
        self.rate = rate
        self.typeRate = typeRate
        self.start = start
        
        self.busy_person = None
        
        self.nextEvent = -1
        self.exit_connectors = []
        
    def generateWork(self, person):
        person.residualWork = np.random.poisson(self.rate)
        
    def receivePerson(self, person):
        if self.busy_person != None:
            return False
        self.busy_person = person
        self.generateWork(person)
        self.nextEvent = self.busy_person.residualWork
        self.busy_person.newWork = True
        return True
        
    def sendPerson(self, person):
        self.busy_person = None
        pass 
        
    def connect_WAIT(self, WAIT_Bubble):
        self.exit_connectors.append(WAIT_Bubble)

    def connect_OUT(self, OUT_Bubble):
        self.exit_connectors.append(OUT_Bubble)

#=================  MAIN CLASSES  =================================        
        
class System:
    def __init__(self, name):
        self.name = name
        self.clock = 0
        self.nextPerson = 0
        
        self.peopleInSystem = 0
        
        self.IN_BubbleList = []
        self.WAIT_BubbleList = []
        self.OUT_BubbleList = []
                
    def create_IN_Bubble(self):
        self.IN_BubbleList.append(IN_Bubble())
        
    def create_WAIT_Bubble(self):
        self.WAIT_BubbleList.append(WAIT_Bubble())
        
    def create_OUT_Bubble(self):
        self.OUT_BubbleList.append(OUT_Bubble())
    
    def connect(self, object1, index1, object2, index2):
        if object1 == "IN_Bubble" and object2 == "WAIT_Bubble":
            self.IN_BubbleList[index1].connect_WAIT(self.WAIT_BubbleList[index2])    
        if object1 == "WAIT_Bubble" and object2 == "OUT_Bubble":
            self.WAIT_BubbleList[index1].connect_OUT(self.OUT_BubbleList[index2])    
    
    
    def startSystem(self):
        #self.checkErrors()
        for item in self.IN_BubbleList:
            item.receivePerson(self.nextPerson, 0)
            self.nextPerson += 1
        
    def run_episode(self, printf):
        number_nextEvent = 999999
        index_nextEvent = 0
        object_nextEvent = ""
        
        for i, item in enumerate(self.IN_BubbleList):
            if number_nextEvent > item.nextEvent and item.nextEvent != -1:
                number_nextEvent = item.nextEvent
                index_nextEvent = i
                object_nextEvent = "IN_Bubble"
        #for i, item in enumerate(self.WAIT_BubbleList):
        #    if number_nextEvent > item.nextEvent and item.nextEvent != -1:
        #        number_nextEvent = item.nextEvent
        #        index_nextEvent = i
        #        object_nextEvent = "WAIT_Bubble"
        for i, item in enumerate(self.OUT_BubbleList):
            if number_nextEvent > item.nextEvent and item.nextEvent != -1:
                number_nextEvent = item.nextEvent
                index_nextEvent = i
                object_nextEvent = "OUT_Bubble"
        
        if object_nextEvent == "IN_Bubble":
            self.IN_BubbleList[index_nextEvent].sendPerson()
        if object_nextEvent == "WAIT_Bubble":
            self.WAIT_BubbleList[index_nextEvent].sendPerson()
        if object_nextEvent == "OUT_Bubble":
            self.OUT_BubbleList[index_nextEvent].sendPerson()
            #passedTime = self.passTime(number_nextEvent)
        
        #Update clock
        passedClock = self.clock
        self.clock = number_nextEvent
        
        self.populate_IN_Bubble()
        self.update_OUT_Bubble(passedClock)
        
        
            
        if printf == True:
            self.printSystemState()
            
    def printSystemState(self):
        print("")
        print("T: " + str(self.clock))
        for i, item in enumerate(self.IN_BubbleList):
            print("IN_" + str(i) + ": " + "|" + str(item.nextPerson.index) + "|" + str(item.nextPerson.arrivalTime) + "|")
        for i, item in enumerate(self.WAIT_BubbleList):
            if item.peopleList:    
                for person in item.peopleList:
                    print("WAIT_" + str(i) + ": " + "|" + str(person.index) + "|" + str(person.arrivalTime) + "|")
            else:
                print("WAIT_" + str(i) + ":")
        for i, item in enumerate(self.OUT_BubbleList):
            if item.busy_person != None:
                print("OUT_" + str(i) + ": " + "|" + str(item.busy_person.index) + "|" + str(item.busy_person.arrivalTime) + "|" + str(item.busy_person.residualWork) + "|" + str(item.busy_person.finishWorkTime))
            else:
                print("OUT_" + str(i) + ":")
        print("")
                       
    #def passTime(self, number_nextEvent):
    #    passedTime = number_nextEvent - self.clock
        
        
    def update_OUT_Bubble(self, passedClock):
        for item in self.OUT_BubbleList:
            if item.busy_person.newWork == False:
                item.busy_person.residualWork = item.busy_person.residualWork - (self.clock - passedClock)
            else:
                item.busy_person.newWork = False
            
    def populate_IN_Bubble(self):
        for item in self.IN_BubbleList:
            if item.nextPerson == None:
                item.receivePerson(self.nextPerson, self.clock)
                self.nextPerson += 1
            
    def checkErrors(self):
        pass
        
class Person:
	def __init__(self, index, arrivalTime):
		self.index = index
		self.arrivalTime = arrivalTime 

		self.residualWork = -1
		self.finishWorkTime = -1
		
		self.newWork = False
#MAIN:
if __name__ == "__main__":
    
    np.random.seed(91)
    
    bank = System("bank")
    bank.create_IN_Bubble()
    bank.create_WAIT_Bubble()
    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
    bank.create_OUT_Bubble()
    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)
    bank.startSystem()
    bank.printSystemState()
    for i in range(2):
        bank.run_episode(True)
    

#bank.createQueue("old")










