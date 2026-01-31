import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

x = list(np.random.rand(19) * 10)
y = list(np.random.rand(19) * 10)

fig, ax = plt.subplots()
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 11)

tolerance = 1
costs = []
visited = []

def calcCost(cX, cY, X, Y, ax):
    minCost = float('inf')
    minInd = -1
    for i, (x, y) in enumerate(zip(X, Y)):
        cost = ((cY-y)**2 + (cX-x)**2)**0.5
        if (cost < minCost):
            minCost = cost
            minInd = i
    ax.arrow(cX, cY, X[minInd]-cX, Y[minInd]-cY,
        color='orange',
        alpha=0.3,
        head_width = 0.1,
        head_length = 0.3,
        length_includes_head=True)


    theta = np.degrees(np.arctan((cY-Y[minInd])/(cX-X[minInd])))
    # ax.text((cX+X[minInd])/2, (cY+Y[minInd])/2, f"{minCost:.2f}",
    # color="orange", fontsize=9, fontweight='bold',
    # ha='center', va='center',
    # rotation = theta, rotation_mode='anchor')
    return minInd


center_x = float(np.random.rand(1) * 10)
center_y = float(np.random.rand(1) * 10)

ax.scatter(x, y)
ax.scatter(center_x, center_y)

start = time.time()
for i in range(19):
    indx = calcCost(center_x, center_y, x, y, ax)
    center_x = x.pop(indx)
    center_y = y.pop(indx)
    visited.append((center_x, center_y))
print(time.time() - start)

plt.show()
