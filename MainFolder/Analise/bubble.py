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
    def __init__(self, rate = 5, typeRate = "Poisson", start = 0, typePerson = None):
        self.rate = rate
        self.typeRate = typeRate
        self.start = start
        self.nextPerson = None
        self.typePerson = typePerson
        self.nextEvent = -1
        self.exit_connectors = []
        self.contador=0

    def sendPerson(self, index_connector = None):
        if index_connector == None:
            index_connector = np.random.randint(len(self.exit_connectors))
        self.exit_connectors[index_connector].receivePerson(self.nextPerson)
        self.nextPerson = None

    def receivePerson(self, index, actualClock):
        if self.typeRate == "Poisson":
            arrivalTime = actualClock + np.random.exponential(1/self.rate)
            #arrivalTime = actualClock + np.random.poisson(self.rate)
        newPerson = Person(index, arrivalTime, self.typePerson)
        self.nextPerson = newPerson
        self.nextEvent = arrivalTime
        return True

    def connect_WAIT(self, WAIT_Bubble):
        self.exit_connectors.append(WAIT_Bubble)

    def connect_OUT(self, OUT_Bubble):
        self.exit_connectors.append(OUT_Bubble)

class WAIT_Bubble:
    def __init__(self, policy = "FIFO", priority=None):
        self.peopleList = []
        self.policy = policy
        self.priority = priority
        self.exit_connectors = []

    def sendPerson(self):
        if self.peopleList:
            person = self.peopleList.pop(0)
            return person
        return None

    def receivePerson(self, person):
        person.lastArrivalTime_wait = person.arrivalTime
        self.alocatePerson(person)
        if person == self.peopleList[0]:
            answer = self.try_OUT(person)
            if answer == True:
                return
            if answer == False:
                for item in self.exit_connectors:
                    item.updateResidualWork(person.arrivalTime)
                return
            else:
                del self.peopleList[0]
                self.alocatePerson(answer)
        else:
            for item in self.exit_connectors:
                item.updateResidualWork(person.arrivalTime)
            return

    def try_OUT(self, person):
        for item in self.exit_connectors:
            if self.priority != None:
                priorityIndex = 0
                for i, j in enumerate(self.priority):
                    if j == person.typePerson:
                        priorityIndex = i
                        break
                priority = self.priority[priorityIndex:]
            else:
                priority = None
            answer = item.receivePerson(person, priority=priority)
            if type(answer) != bool:
                return answer
            elif answer == True:
                del self.peopleList[0]
                return True
            else:
                return False

    def alocatePerson(self, person):
        if not self.peopleList:
            self.peopleList.append(person)
            return
        if self.policy == "FIFO" or self.policy == "FCFS":
            if self.priority == None:
                self.peopleList.append(person)
                return
            else:
                priorityIndex = 0
                for i, item in enumerate(self.priority):
                    if item == person.typePerson:
                        priorityIndex = i
                        break
                for i, item in enumerate(self.peopleList):
                    if item.typePerson in self.priority[priorityIndex:]:
                        self.peopleList.insert(i, person)
                        return
        if self.policy == "LCFS":
            self.peopleList.insert(0, person)


    def getPosition(self, person):
        classPerson = person.typePerson
        mainPriority = priority[0]
        if classPerson == mainPriority:
            for i, item in self.peopleList:
                if item.typePerson == classPerson:
                    return i
    def connect_OUT(self, OUT_Bubble):
        OUT_Bubble.entrance_connectors.append(self)
        self.exit_connectors.append(OUT_Bubble)

class OUT_Bubble:
    def __init__(self, rate = 5, typeRate = "Poisson", start = 0, preemption = False):
        self.rate = rate
        self.typeRate = typeRate
        self.start = start
        self.preemption = preemption
        self.busy_person = None

        self.nextEvent = -1
        self.entrance_connectors = []
        self.exit_connectors = []

    def sendPerson(self):
        finishWorklastBusyPerson = self.busy_person.finishWorkTime
        self.busy_person = None

        #ask from wait:
        randomChoice = np.random.randint(len(self.entrance_connectors))
        person = self.entrance_connectors[randomChoice].sendPerson()
        if person != None:
            self.receivePerson(person, finishWorklastBusyPerson)
            return True
        else:
            self.nextEvent = -1
            return False

    def receivePerson(self, person, finishWorklastBusyPerson=None, priority=None):
        returnedPerson = copy.deepcopy(self.busy_person)
        if self.busy_person == None:
            self.busy_person = person
            self.generateWork(self.busy_person)
            self.nextEvent = self.busy_person.residualWork
            if finishWorklastBusyPerson != None:
                self.busy_person.lastArrivalTime_wait = finishWorklastBusyPerson
            return True
        else:
            if self.preemption == False:
                return False
            else:
                if priority == None or self.busy_person.typePerson in priority:
                    returnedPerson.finishWorkTime = -1
                    returnedPerson.lastArrivalTime_wait = person.arrivalTime
                    returnedPerson.residualWork -= person.arrivalTime - self.busy_person.lastArrivalTime_wait

                    self.busy_person = person
                    self.generateWork(person)
                    self.nextEvent = self.busy_person.residualWork
                    return returnedPerson
                else:
                    return False

    def updateResidualWork(self, arrivalTime):
        if self.busy_person.residualFlag == False:

        #if self.preemption == True:
            self.busy_person.residualWork = (self.busy_person.finishWorkTime - arrivalTime)
        #if self.preemption == False:


    def generateWork(self, person):
        if person.residualWork == -1:
            person.residualWork = np.random.exponential(1/self.rate)
            person.residualFlag = True
            #person.residualWork = np.random.poisson(self.rate)
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

    def create_IN_Bubble(self, typePerson=None,ratePar=5):
        self.IN_BubbleList.append(IN_Bubble(rate = ratePar,typePerson=typePerson))

    def create_WAIT_Bubble(self, policy="FIFO", priority=None):
        self.WAIT_BubbleList.append(WAIT_Bubble(policy=policy, priority=priority))

    def create_OUT_Bubble(self, preemption=False,ratePar=5):
        self.OUT_BubbleList.append(OUT_Bubble(rate = ratePar,preemption=preemption))

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
            #self.printSystemState()
            return self.saveInString()
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

    def saveInString(self):
        string = "\n"
        string += "T: " + str(self.clock) + "\n"
        for i, item in enumerate(self.IN_BubbleList):
            string += "IN_" + str(i) + item.nextPerson.printPerson() + "\n"

        for i, item in enumerate(self.WAIT_BubbleList):
            if item.peopleList:
                for person in item.peopleList:
                    string += "WAIT_" + str(i) + person.printPerson() + "\n"
            else:
                string += "WAIT_" + str(i) + ":" + "\n"

        for i, item in enumerate(self.WAIT_BubbleList):
            if item.peopleList:
                for person in item.peopleList:
                    string += "WAIT_" + str(i) + person.printPerson() + "\n"
            else:
                string += "WAIT_" + str(i) + ":" + "\n"

        for i, item in enumerate(self.OUT_BubbleList):
            if item.busy_person != None:
                string += "OUT_" + str(i) + item.busy_person.printPerson() + "\n"
            else:
                string += "OUT_" + str(i) + ":" + "\n"
        string += "\n"
        return string


    def printSystemState(self):
        print("")

        print("T: " + str(self.clock))

        for i, item in enumerate(self.IN_BubbleList):
            print("IN_" + str(i) + item.nextPerson.printPerson())

        for i, item in enumerate(self.WAIT_BubbleList):
            if item.peopleList:
                for person in item.peopleList:
                    print("WAIT_" + str(i) + person.printPerson())
            else:
                print("WAIT_" + str(i) + ":")

        for i, item in enumerate(self.OUT_BubbleList):
            if item.busy_person != None:
                print("OUT_" + str(i) + item.busy_person.printPerson())
            else:
                print("OUT_" + str(i) + ":")
        print("")

    def update_OUT_Bubble(self, previousClock):
        for item in self.OUT_BubbleList:
            if item.busy_person != None:
                if item.busy_person.residualWork != -1:
                    item.busy_person.finishWorkTime = item.busy_person.residualWork + self.clock
                    item.busy_person.residualFlag = False
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
    def __init__(self, index, arrivalTime, typePerson ):
        self.typePerson = typePerson
        self.index = index
        self.arrivalTime = arrivalTime

        self.residualFlag = True

        self.residualWork = -1
        self.finishWorkTime = -1
        self.lastArrivalTime_wait = -1

    def printPerson(self):
        string = ": |" + str(self.typePerson) + "|" + str(self.index) + "|" + str(self.arrivalTime) + "|" + str(self.residualWork) + "|" + str(self.finishWorkTime) + "|" + str(self.lastArrivalTime_wait) + "|"
        return string
