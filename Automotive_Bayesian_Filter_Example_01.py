from __future__ import print_function, division
import matplotlib.pyplot as plt
import bar_plot
import numpy as np

pos = np.array([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1])
hallway = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 0])

def normalize(p):
	s = sum(p)
	for i in range (len(p)):
		p[i] = p[i] / s
def update(pos, measure, p_hit, p_miss):
	q = np.array(pos, dtype=float)
	for i in range(len(hallway)):
		if hallway[i] == measure:
		q[i] = pos[i] * p_hit
		else:
		q[i] = pos[i] * p_miss
	normalize(q)
	return q


def predict(pos, move, p_correct, p_under, p_over):
	n = len(pos)
	result = np.array(pos, dtype=float)
	for i in range(n):
		result[i] = \
		pos[(i-move) % n] * p_correct + \
		pos[(i-move-1) % n] * p_over + \
		pos[(i-move+1) % n] * p_under
	return result

#This is another fairly hallway example.
#hallway = [1,0,1,0,0,1,0,1,0,0]
#pos = np.array([.1]*10)
measurements = [1,0,1,0,0]
for m in measurements:
	pos = update(pos, m, .6, .2)
	pos = predict(pos, 1, .8, .1, .1)
	bar_plot.plot(pos)
print(pos)
