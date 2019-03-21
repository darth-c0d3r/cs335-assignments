from State import State

class MDP:
	
	def __init__(self, filename=None):

		self.file = filename

		self.numStates = None
		self.numActions = None
		self.startState = None
		self.endStates = []
		self.allStates = []
		self.gamma = None

		self.optValues = None
		self.optPolicy = None
		self.numIter = None

	def buildMDP(self):

		allLines = None
		with open(self.file, 'r') as file:
			allLines = file.readlines()

		self.numStates = int(allLines[0].split()[-1])
		self.numActions = int(allLines[1].split()[-1])
		self.startState = int(allLines[2].split()[-1])

		endStates = allLines[3].split()[1:]
		endStates = [int(state) for state in endStates]
		if endStates[0] != -1:
			self.endStates = endStates

		self.allStates = [None] * self.numStates
		for idx in range(len(self.allStates)):
			self.allStates[idx] = State(idx, self.numActions)

		for idx in range(4,len(allLines)-1):
			trx = allLines[idx].split()[1:]
			for idx in range(len(trx)-2):
				trx[idx] = int(trx[idx])
			for idx in range(1,3):
				trx[-idx] = float(trx[-idx])
			
			self.allStates[trx[0]].addTransition(trx)

		self.gamma = float(allLines[-1].split()[-1])

	def printMDP(self):

		print("numStates", self.numStates)
		print("numActions", self.numActions)
		print("start", self.startState)
		if len(self.endStates) == 0:
			print("end",-1)
		else:
			print("end", str(self.endStates)[1:-1])
		for state in self.allStates:
			state.printState()
		print("discount",self.gamma)


	def getOptimalValues(self):

		epsilon = 1e-16

		self.optValues = [float(0)]*self.numStates
		self.numIter = 0

		converge = False
		while converge is False:
			converge = True
			for state in self.allStates:
				if state.idx in self.endStates:
					continue
				currValues = [float(0)] * self.numActions

				for idx, actions in enumerate(state.transitions):
					for trx in actions:
						currValues[idx] += (trx[2] * (trx[1] + (self.gamma * self.optValues[trx[0]])))

				newValue = max(currValues)
				if abs(self.optValues[state.idx]-newValue) > epsilon:
					converge = False

				self.optValues[state.idx] = newValue

			self.numIter += 1

	def getOptimalPolicy(self):

		self.optPolicy = [-1]*self.numStates

		for state in self.allStates:
			if state.idx in self.endStates:
				continue
			currValue = -float("inf")
			currIdx = -1
			for idx, actions in enumerate(state.transitions):
				currValueTemp = float(0)
				for trx in actions:
					currValueTemp += (trx[2] * (trx[1] + (self.gamma * self.optValues[trx[0]])))
				if currValueTemp > currValue:
					currValue = currValueTemp
					currIdx = idx

			self.optPolicy[state.idx] = currIdx

	def printResult(self):
		for idx in range(self.numStates):
			print(round(self.optValues[idx],11), self.optPolicy[idx])
		print("iterations",self.numIter)


