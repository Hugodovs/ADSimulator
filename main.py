#import numpy as np

#Save file
with open("queue1.txt", "r") as f:
	scenario = f.read().split(";")	

arrivalsTime = []
for number in scenario[0].split(" "):
	arrivalsTime.append(int(number))

worksLoad = []
for number in scenario[1].split(" "):
	worksLoad.append(int(number))

class Person:
	def __init__(index, residualWork, queue):
		self.index = index
		self.residualWork = residualWork
		self.queue = queue
		self.globalArrivalTime = self.queue.clock + arrivalsTime[self.index]	
		
	def getIndex(self):
		return self.index

	def getResidualWork(self):
		return self.residualWork

class Queue:
	def __init__(clock):
		self.clock = clock
		self.waitQueue = []				#Array of Person
		self.serverPerson = None		#One Person
		self.nextPerson = Person(0, worksLoad[0], self) 

#Init Queue:
queue = Queue(0)

while (True):

	
	if (
	lastPersonId = 0 	#Last person id that arrived in the queue

	#Person, arrival 

	if (nextPerson
	nextPerson = Person(lastPersonId, 
	
	nextArrival = arrivalsTime()
	actualWork = 

