import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

DEFAULT_TOLERANCE = 5
Path = []

#all costs -> distance**2

class savedState:
    def __init__(self, X : np.array, Y : np.array, source_point, cost, visited : list, tolerance = 0, toVisit : list = None): #note: only use toVisit if you want to manually add a point you want the algorithm to visit
        self.cost = cost
        self.X = X.copy()
        self.Y = Y.copy()
        self.source = source_point
        self.visited = visited.copy() #ordered list detailing path until reaching saved state

        if toVisit is None:  #localized whitelisted points
            self.toVisit = []
        else:
            self.toVisit = toVisit.copy()
        
        if (X.size != 0) and (not tolerance):
            self.scan(DEFAULT_TOLERANCE)
        elif X.size != 0:
            self.scan(tolerance)
        else:
            pass
    def scan(self, tolerance):
        costs = []
        for x, y in zip(self.X, self.Y):
            costs.append((self.source[0] - x)**2 + (self.source[1] - y)**2)
        if costs:
            minCost = min(costs)
            self.toVisit = [(x, y) for x, y, cost in zip(self.X, self.Y, costs) if (cost <= (minCost*tolerance))] 

savedStates = []
completedPaths = []

nodes = 20

x = np.random.rand(nodes - 1) * 10
y = np.random.rand(nodes - 1) * 10

print(x)
print(y)

costSum = 0

copyX = list(x)
copyY = list(y)

fig, ax = plt.subplots(1, 2, figsize = (12, 6))
ax[0].set_xlim(-1, 11)
ax[0].set_ylim(-1, 11)
ax[1].set_xlim(-1, 11)
ax[1].set_ylim(-1, 11)


source_x = 1.87343
source_y = 8.23431

ax[0].scatter(source_x, source_y, color = "orange")
ax[1].scatter(source_x, source_y, color = "orange")

savedStates.append(savedState(x, y, (source_x, source_y), 0, [(float(source_x), float(source_y))])) #initializes the first saved state
# print(savedStates[0].X)
# print(savedStates[0].Y)
# print(savedStates[0].toVisit)
# print(savedStates[0].visited)
# print(savedStates[0].cost)
start = time.perf_counter()
while True:
    currState = savedStates.pop()
    if (currState.toVisit):
        while currState.toVisit:
            visiting = currState.toVisit.pop()
            mask = ~((currState.X == visiting[0]) & (currState.Y == visiting[1]))
            savedStates.append(savedState(currState.X[mask], currState.Y[mask],
                                        (visiting[0], visiting[1]),
                                        currState.cost + ((currState.source[0] - visiting[0])**2 + (currState.source[1] - visiting[1])**2),
                                        currState.visited + [visiting],))
    else:
        completedPaths.append(currState)
    if not savedStates:
        break
print(f"Time taken : {time.perf_counter() - start}")
minPath = completedPaths[0]
for path in completedPaths:
    if (path.cost < minPath.cost) : minPath = path

def calcCost(cX, cY, X, Y, ax):
    global costSum
    minCost = float('inf')
    minInd = -1
    for i, (x, y) in enumerate(zip(X, Y)):
        cost = ((cY-y)**2 + (cX-x)**2)
        if (cost < minCost):
            minCost = cost
            minInd = i
    costSum += minCost
    return minInd

Path.append((source_x, source_y))
for i in range(nodes - 1):
    indx = calcCost(source_x, source_y, copyX, copyY, ax)
    source_x = copyX.pop(indx)
    source_y = copyY.pop(indx)
    Path.append((source_x, source_y))


print(f"Optimized => Path with minimum cost: {[(float(x), float(y)) for x, y in minPath.visited]}, Cost: {minPath.cost}\nUnoptimized => Path with minimum cost: {[(float(x), float(y)) for x, y in Path]}, Cost: {costSum}")

optX, optY = zip(*minPath.visited)
unOptX, unOptY = zip(*Path)

ax[0].set_title("Optimized pathing")
ax[1].set_title("Unoptimized pathing")

ax[0].scatter(optX[1:], optY[1:])
ax[1].scatter(unOptX[1:], unOptY[1:])

for i in range(0, nodes - 1):
    ax[0].arrow(optX[i], optY[i], optX[i+1]-optX[i], optY[i+1]-optY[i],
    color='orange',
    alpha=0.3,
    head_width = 0.1,
    head_length = 0.3,
    length_includes_head=True)

for i in range(0, nodes - 1):
    ax[1].arrow(unOptX[i], unOptY[i], unOptX[i+1]-unOptX[i], unOptY[i+1]-unOptY[i],
    color='orange',
    alpha=0.3,
    head_width = 0.1,
    head_length = 0.3,
    length_includes_head=True)

plt.show()
