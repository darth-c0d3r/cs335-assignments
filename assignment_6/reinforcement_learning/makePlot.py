import matplotlib.pyplot as plt
import os

folder = "paths/"
files = os.listdir(folder)

probs = []
values = []

for file in files:
	with open(folder+file,'r') as f:
		value = len(f.readlines()[0].split())
		probs.append(file)
		values.append(value)

plt.plot(probs,values)
plt.show()

