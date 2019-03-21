from MDP import MDP
import sys

mdp = MDP(sys.argv[1])
mdp.buildMDP()
# mdp.printMDP()
mdp.getOptimalValues()
mdp.getOptimalPolicy()
mdp.printResult()