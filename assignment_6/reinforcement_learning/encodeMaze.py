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
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i-1][j]), -1,1])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i-1][j]), -1,1])

			if states[i][j+1] != -1:
				if maze[i][j+1] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j+1]), -1,1])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j+1]), -1,1])

			if states[i+1][j] != -1:
				if maze[i+1][j] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i+1][j]), -1,1])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i+1][j]), -1,1])

			if states[i][j-1] != -1:
				if maze[i][j-1] == 3:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j-1]), -1,1])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j-1]), -1,1])

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
			valid = [None]*4
			valid[0] = (states[i-1][j] != -1)
			valid[1] = (states[i][j+1] != -1)
			valid[2] = (states[i+1][j] != -1)
			valid[3] = (states[i][j-1] != -1)
			goal = [None]*4
			goal[0] = (maze[i-1][j] == 3)
			goal[1] = (maze[i][j+1] == 3)
			goal[2] = (maze[i+1][j] == 3)
			goal[3] = (maze[i][j-1] == 3)

			if valid[0]:
				if goal[0]:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i-1][j]), -1,p+((1.0-p)/validStates)])
					if valid[1]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i-1][j]), -1,(1.0-p)/validStates])
					if valid[2]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i-1][j]), -1,(1.0-p)/validStates])
					if valid[3]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i-1][j]), -1,(1.0-p)/validStates])					
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i-1][j]), -1,p+(1.0-p)/validStates])
					if valid[1]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i-1][j]), -1,(1.0-p)/validStates])
					if valid[2]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i-1][j]), -1,(1.0-p)/validStates])
					if valid[3]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i-1][j]), -1,(1.0-p)/validStates])

			if valid[1]:
				if goal[1]:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j+1]), -1,p+((1.0-p)/validStates)])
					if valid[0]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i][j+1]), -1,(1.0-p)/validStates])
					if valid[2]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i][j+1]), -1,(1.0-p)/validStates])
					if valid[3]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j+1]), -1,(1.0-p)/validStates])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j+1]), -1,p+(1.0-p)/validStates])
					if valid[0]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i][j+1]), -1,(1.0-p)/validStates])
					if valid[2]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i][j+1]), -1,(1.0-p)/validStates])
					if valid[3]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j+1]), -1,(1.0-p)/validStates])

			if valid[2]:
				if goal[2]:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i+1][j]), -1,p+((1.0-p)/validStates)])
					if valid[0]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i+1][j]), -1,(1.0-p)/validStates])
					if valid[1]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i+1][j]), -1,(1.0-p)/validStates])
					if valid[3]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i+1][j]), -1,(1.0-p)/validStates])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i+1][j]), -1,p+((1.0-p)/validStates)])
					if valid[0]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i+1][j]), -1,(1.0-p)/validStates])
					if valid[1]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i+1][j]), -1,(1.0-p)/validStates])
					if valid[3]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i+1][j]), -1,(1.0-p)/validStates])

			if valid[3]:
				if goal[3]:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j-1]), -1,p+((1.0-p)/validStates)])
					if valid[0]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i][j-1]), -1,(1.0-p)/validStates])
					if valid[1]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j-1]), -1,(1.0-p)/validStates])
					if valid[2]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i][j-1]), -1,(1.0-p)/validStates])
				else:
					mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 3, int(states[i][j-1]), -1,p+((1.0-p)/validStates)])
					if valid[0]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 0, int(states[i][j-1]), -1,(1.0-p)/validStates])
					if valid[1]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 1, int(states[i][j-1]), -1,(1.0-p)/validStates])
					if valid[2]:
						mdp.allStates[int(states[i][j])].addTransition([int(states[i][j]), 2, int(states[i][j-1]), -1,(1.0-p)/validStates])

	mdp.gamma = 1
	return mdp

if __name__ == '__main__':
	if len(sys.argv) == 2:
		encodeMazeDeterministic(sys.argv[1]).printMDP()
	else:
		encodeMazeProbabilistic(sys.argv[1], float(sys.argv[2])).printMDP()

