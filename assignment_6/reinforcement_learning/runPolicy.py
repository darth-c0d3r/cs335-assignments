from MDP import MDP
from encodeMaze import encodeMazeDeterministic
from encodeMaze import encodeMazeProbabilistic
import sys
import numpy as np

def readPolicyFile(policy_file):
	lines = None
	with open(policy_file,'r') as file:
		lines = file.readlines()
	lines = lines[:-1]
	lines = [int(line.split()[-1]) for line in lines]

	return lines

def runPolicyDeterministic(grid_file, policy_file):

	mdp = encodeMazeDeterministic(grid_file)
	actions = readPolicyFile(policy_file)

	currState = mdp.allStates[mdp.startState]
	allActions = []
	while currState.idx not in mdp.endStates:
		allActions.append(actions[currState.idx])
		currState = mdp.allStates[currState.transitions[actions[currState.idx]][0][0]]

	actionMap = ['N','E','S','W']
	allActions = [actionMap[idx] for idx in allActions]
	for action in allActions:
		print(action, end=' ')
	print()

def getAction(mdp, prev, curr):
	for idx, action in enumerate(mdp.allStates[prev].transitions):
		if len(action) == 1 and action[0][0] == curr:
			return idx

def runPolicyProbabilistic(grid_file, policy_file,p):
	mdp_ = encodeMazeDeterministic(grid_file)
	mdp = encodeMazeProbabilistic(grid_file,p)
	actions = readPolicyFile(policy_file)

	currState = mdp.allStates[mdp.startState]
	allActions = []
	while currState.idx not in mdp.endStates:
		prevState = currState
		allStates = currState.transitions[actions[currState.idx]]
		allProbab = [state[-1] for state in allStates]
		allStates = [state[0] for state in allStates]
		currState = np.random.choice(allStates, p=allProbab)
		currState = mdp.allStates[currState]

		allActions.append(getAction(mdp_,prevState.idx,currState.idx))

	actionMap = ['N','E','S','W']
	allActions = [actionMap[idx] for idx in allActions]
	for action in allActions:
		print(action, end=' ')
	print()


if __name__ == '__main__':
	if len(sys.argv) == 3:
		runPolicyDeterministic(sys.argv[1], sys.argv[2])
	else:
		runPolicyProbabilistic(sys.argv[1], sys.argv[2], float(sys.argv[3]))


