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
import copy

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
            arrivalTime = actualClock + np.random.exponential(1/self.rate)
        newPerson = Person(index, arrivalTime)

        self.nextPerson = newPerson
        self.nextEvent = arrivalTime
        return True

    def sendPerson(self, index_connector = None):
        if index_connector == None:
            index_connector = np.random.randint(len(self.exit_connectors))
        self.exit_connectors[index_connector].receivePerson(self.nextPerson)
        self.nextPerson = None

    def connect_WAIT(self, WAIT_Bubble):
        self.exit_connectors.append(WAIT_Bubble)

    def connect_OUT(self, OUT_Bubble):
        self.exit_connectors.append(OUT_Bubble)

class WAIT_Bubble:
    def __init__(self, policy = "FIFO", preemption=False):
        self.peopleList = []
        self.preemption = preemption
        self.policy = policy
        self.exit_connectors = []

    def receivePerson(self, person):
        status = self.try_OUT(person)
        if status == True:
            return

        if self.policy == "FIFO" or self.policy == "FCFS":
            self.peopleList.append(person)
        if self.policy == "LCFS":
            self.peopleList.insert(0, person)
        return

    def try_OUT(self, person):
        for item in self.exit_connectors:
            status = item.receivePerson(person)
            if status == True:
                return True
        return False

    def sendPerson(self):
        if self.peopleList:
            person = self.peopleList.pop(0)
            return person
        return None

    def connect_OUT(self, OUT_Bubble):
        OUT_Bubble.entrance_connectors.append(self)
        self.exit_connectors.append(OUT_Bubble)

class OUT_Bubble:
    def __init__(self, rate = 6, typeRate = "Poisson", start = 0):
        self.rate = rate
        self.typeRate = typeRate
        self.start = start

        self.busy_person = None

        self.nextEvent = -1
        self.entrance_connectors = []
        self.exit_connectors = []

    def generateWork(self, person):
        person.residualWork = np.random.exponential(1/self.rate)

    def receivePerson(self, person):
        if self.busy_person != None:
            return False
        self.busy_person = person
        self.generateWork(person)
        self.nextEvent = self.busy_person.residualWork
        self.busy_person.newWork = True
        return True

    def sendPerson(self):
        self.busy_person = None

        #ask for wait:
        randomChoice = np.random.randint(len(self.entrance_connectors))
        person = self.entrance_connectors[randomChoice].sendPerson()
        if person != None:
            self.receivePerson(person)
        else:
            self.nextEvent = -1

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

    def create_WAIT_Bubble(self, policy="FIFO", preemption=False):
        self.WAIT_BubbleList.append(WAIT_Bubble(policy=policy, preemption=preemption))

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

    def run_episode(self, printstates = False):
        number_nextEvent = 999999
        index_nextEvent = []
        object_nextEvent = []

        #Get next events:
        for i, item in enumerate(self.IN_BubbleList):
            if number_nextEvent > item.nextEvent and item.nextEvent != -1:
                number_nextEvent = item.nextEvent
                index_nextEvent = [i]
                object_nextEvent = ["IN_Bubble"]
            elif number_nextEvent == item.nextEvent and item.nextEvent != -1:
                index_nextEvent.append(i)
                object_nextEvent.append("IN_Bubble")
        for i, item in enumerate(self.OUT_BubbleList):
            if number_nextEvent > item.nextEvent and item.nextEvent != -1:
                number_nextEvent = item.nextEvent
                index_nextEvent = [i]
                object_nextEvent = ["OUT_Bubble"]
            elif number_nextEvent == item.nextEvent and item.nextEvent != -1:
                index_nextEvent.append(i)
                object_nextEvent.append("OUT_Bubble")

        #OUT first, then IN:
        new_index_nextEvent = []
        new_object_nextEvent = []
        for i, item in enumerate(object_nextEvent):
            if item == "OUT_Bubble":
                new_object_nextEvent.append("OUT_Bubble")
                new_index_nextEvent.append(index_nextEvent[i])
        for i, item in enumerate(object_nextEvent):
            if item == "IN_Bubble":
                new_object_nextEvent.append("IN_Bubble")
                new_index_nextEvent.append(index_nextEvent[i])
        index_nextEvent = new_index_nextEvent
        object_nextEvent = new_object_nextEvent

        #Act next events:
        for i, item in enumerate(object_nextEvent):
            if item == "IN_Bubble":
                self.IN_BubbleList[index_nextEvent[i]].sendPerson()
            if item == "WAIT_Bubble":
                self.WAIT_BubbleList[index_nextEvent[i]].sendPerson()
            if item == "OUT_Bubble":
                self.OUT_BubbleList[index_nextEvent[i]].sendPerson()



        #Update clock
        previousClock = self.clock
        self.clock = number_nextEvent

        self.populate_IN_Bubble()
        self.update_OUT_Bubble(previousClock)

        if printstates == True:
            self.printSystemState()
            #self.printNextEvent()

    def printNextEvent(self):
        print("")
        print("nextEvents: ")
        for i, item in enumerate(self.IN_BubbleList):
            print("IN")
            print(item.nextEvent)

        for i, item in enumerate(self.OUT_BubbleList):
            print("OUT")
            print(item.nextEvent)


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

    def update_OUT_Bubble(self, previousClock):
        for item in self.OUT_BubbleList:
            if item.busy_person != None:
                if item.busy_person.newWork == True:
                    item.busy_person.newWork = False
                    item.busy_person.finishWorkTime = item.busy_person.residualWork + self.clock
                else:
                    item.busy_person.residualWork -= (self.clock - previousClock)
                item.nextEvent = item.busy_person.finishWorkTime

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

    np.random.seed(105)

    bank = System("bank")
    bank.create_IN_Bubble()
    bank.create_WAIT_Bubble(policy="LCFS", preemption=True)
    bank.connect("IN_Bubble", 0, "WAIT_Bubble", 0)
    bank.create_OUT_Bubble()
    bank.connect("WAIT_Bubble", 0, "OUT_Bubble", 0)
    bank.startSystem()
    bank.printSystemState()

    for i in range(100):
        bank.run_episode(printstates = True)


#bank.createQueue("old")
