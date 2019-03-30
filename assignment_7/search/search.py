import util
from sudoku import SudokuSearchProblem
from maps import MapSearchProblem

################ Node structure to use for the search algorithm ################
class Node:
	def __init__(self, state, action, path_cost, parent_node, depth):
		self.state = state
		self.action = action
		self.path_cost = path_cost
		self.parent_node = parent_node
		self.depth = depth

########################## DFS for Sudoku ########################
## Choose some node to expand from the frontier with Stack like implementation
def sudokuDepthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.
	Return the final values dictionary, i.e. the values dictionary which is the goal state  
	"""

	def convertStateToHash(values):
		""" 
		values as a dictionary is not hashable and hence cannot be used directly in the explored/visited set.
		This function changes values dict into a unique hashable string which can be used in the explored set.
		You may or may not use this
		"""
		l = list(sorted(values.items()))
		modl = [a+b for (a, b) in l]
		return ''.join(modl)

	
	frontier = util.Stack()

	frontier.push(problem.start_values.copy())

	while frontier.isEmpty() is False:
		curr_node = frontier.pop()
		if problem.isGoalState(curr_node):
			return curr_node
		children = problem.getSuccessors(curr_node)
		for node in children:
			frontier.push(node[0])

	return False
	## YOUR CODE HERE
	# util.raiseNotDefined()

######################## A-Star and DFS for Map Problem ########################
## Choose some node to expand from the frontier with priority_queue like implementation

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def heuristic(state, problem):
	# It would take a while for Flat Earther's to get accustomed to this paradigm
	# but hang in there.

	"""
		Takes the state and the problem as input and returns the heuristic for the state
		Returns a real number(Float)
	"""
		
	curr = problem.G.node[state]
	end = problem.G.node[problem.end_node]
	return util.points2distance(((curr['x'],0,0), (curr['y'],0,0)), ((end['x'],0,0), (end['y'],0,0)))


def AStar_search(problem, heuristic=nullHeuristic):

	"""
		Search the node that has the lowest combined cost and heuristic first.
		Return the route as a list of nodes(Int) iterated through starting from the first to the final.
	"""

	frontier = util.PriorityQueue()
	explored_set = list()

	# state, action, path_cost, parent_node, depth
	frontier.push(Node(problem.start_node, None, 0, None, 0), 0)
	parents = {}

	path = []

	while frontier.isEmpty() is False:
		curr_node = frontier.pop()

		if curr_node.state in explored_set:
			continue
		explored_set.append(curr_node.state)

		parents[curr_node.state] = curr_node.parent_node

		if problem.isGoalState(curr_node.state):
			curr_node = curr_node.state
			path.append(curr_node)
			while True:
				if parents[curr_node] is None:
					path.reverse()
					break
				path.append(parents[curr_node])
				curr_node = parents[curr_node]
			break

		children = problem.getSuccessors(curr_node.state)
		for child in children:
			frontier.update(Node(child[0], child[1], curr_node.path_cost + child[2], curr_node.state, curr_node.depth+1), 
				curr_node.path_cost + child[2] + heuristic(child[0], problem))

	return path




	# util.raiseNotDefined()