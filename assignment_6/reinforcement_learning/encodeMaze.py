import numpy as np
import sys
from MDP import MDP
from State import State

def encodeMazeDeterministic(filename):

	maze = None
	with open(filename, 'r') as file:
		maze = file.readlines()

	maze = [line.split() for line in maze]
	maze = [[int(num) for num in line] for line in maze]
	maze = np.array(maze)

	currState = 0
	startState = -1
	endState = -1

	states = np.zeros(maze.shape)

	for i in range(len(states)):
		for j in range(len(states[i])):
			if maze[i][j] != 1:
				states[i][j] = currState
				currState += 1
			else:
				states[i][j] = -1
				continue

			if maze[i][j] == 2:
				startState = currState-1
			if maze[i][j] == 3:
				endState = currState-1

	mdp = MDP()

	mdp.numStates = currState
	mdp.numActions = 4
	mdp.startState = startState
	mdp.endStates = [endState]
	mdp.allStates = [None] * mdp.numStates

	for idx in range(len(mdp.allStates)):
		mdp.allStates[idx] = State(idx, mdp.numActions)

	for i in range(len(maze)):
		for j in range(len(maze[i])):

			if states[i][j] == -1:
				continue
			
			if states[i-1][j] != -1:
				if maze[i-1][j] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i-1][j]), 1000,1])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i-1][j]), 1,1])

			if states[i][j+1] != -1:
				if maze[i][j+1] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j+1]), 1000,1])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j+1]), 1,1])

			if states[i+1][j] != -1:
				if maze[i+1][j] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i+1][j]), 1000,1])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i+1][j]), 1,1])

			if states[i][j-1] != -1:
				if maze[i][j-1] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j-1]), 1000,1])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j-1]), 1,1])

	mdp.gamma = 0.9
	return mdp

def encodeMazeProbabilistic(filename, p=1):

	maze = None
	with open(filename, 'r') as file:
		maze = file.readlines()

	maze = [line.split() for line in maze]
	maze = [[int(num) for num in line] for line in maze]
	maze = np.array(maze)

	currState = 0
	startState = -1
	endState = -1

	states = np.zeros(maze.shape)

	for i in range(len(states)):
		for j in range(len(states[i])):
			if maze[i][j] != 1:
				states[i][j] = currState
				currState += 1
			else:
				states[i][j] = -1
				continue

			if maze[i][j] == 2:
				startState = currState-1
			if maze[i][j] == 3:
				endState = currState-1

	mdp = MDP()

	mdp.numStates = currState
	mdp.numActions = 4
	mdp.startState = startState
	mdp.endStates = [endState]
	mdp.allStates = [None] * mdp.numStates

	for idx in range(len(mdp.allStates)):
		mdp.allStates[idx] = State(idx, mdp.numActions)

	for i in range(len(maze)):
		for j in range(len(maze[i])):

			if states[i][j] == -1:
				continue
			
			validStates = float(int(states[i-1][j]!=-1)+int(states[i+1][j]!=-1)+int(states[i][j-1]!=-1)+int(states[i][j+1]!=-1))

			if states[i-1][j] != -1:
				if maze[i-1][j] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i-1][j]), 1000,p+(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i-1][j]), 1000,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i-1][j]), 1000,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i-1][j]), 1000,(1.0-p)/validStates])					
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i-1][j]), 1,p+(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i-1][j]), 1,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i-1][j]), 1,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i-1][j]), 1,(1.0-p)/validStates])

			if states[i][j+1] != -1:
				if maze[i][j+1] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j+1]), 1000,p+(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i][j+1]), 1000,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i][j+1]), 1000,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j+1]), 1000,(1.0-p)/validStates])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j+1]), 1,p+(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i][j+1]), 1,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i][j+1]), 1,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j+1]), 1,(1.0-p)/validStates])

			if states[i+1][j] != -1:
				if maze[i+1][j] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i+1][j]), 1000,p+(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i+1][j]), 1000,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i+1][j]), 1000,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i+1][j]), 1000,(1.0-p)/validStates])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i+1][j]), 1,p+(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i+1][j]), 1,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i+1][j]), 1,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i+1][j]), 1,(1.0-p)/validStates])

			if states[i][j-1] != -1:
				if maze[i][j-1] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j-1]), 1000,p+(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i][j-1]), 1000,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j-1]), 1000,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i][j-1]), 1000,(1.0-p)/validStates])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j-1]), 1,p+(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i][j-1]), 1,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j-1]), 1,(1.0-p)/validStates])
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i][j-1]), 1,(1.0-p)/validStates])

	mdp.gamma = 0.9
	return mdp

if __name__ == '__main__':
	if len(sys.argv) == 2:
		encodeMazeDeterministic(sys.argv[1]).printMDP()
	else:
		encodeMazeProbabilistic(sys.argv[1], float(sys.argv[2])).printMDP()

