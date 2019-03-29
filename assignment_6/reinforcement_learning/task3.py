import os

probs = [str(i/10) for i in range(11)]

for p in probs:
	os.system("./encoder.sh data/maze/grid20.txt " + p + " > temp/mdp_20_" + p)
	os.system("./valueiteration.sh temp/mdp_20_" + p + " > temp/policy_20_" + p)
	os.system("./decoder.sh data/maze/grid20.txt temp/policy_20_" + p + " " + p + " > paths/" + p)
	print(p,"done")
