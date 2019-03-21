class State:

	def __init__(self, idx, numActions):

		self.idx = idx
		self.transitions = [[] for _ in range(numActions)]

	def addTransition(self, valueArray):

		assert(len(valueArray) == 5)
		assert(valueArray[0] == self.idx)

		self.transitions[valueArray[1]].append((valueArray[2], valueArray[3], valueArray[4]))

	def printState(self):
		for idx, actions in enumerate(self.transitions):
			for trx in actions:
				print("transition",self.idx,idx,trx[0],trx[1],trx[2])