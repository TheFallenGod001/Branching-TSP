import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

DEFAULT_TOLERANCE = 1.8
Path = []
costSum = 0
#all costs -> distance**2

optMinCosts1 = []
optTime1 = []
optMinCosts2 = []
optTime2 = []
optMinCosts3 = []
optTime3 = []
optMinCosts4 = []
optTime4 = []
optTolerances = []

unoptMinCosts = []
unoptTime = []

fig, axes = plt.subplots(2)

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

def calcCost(cX, cY, X, Y):
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

for j in range(10):
    print(f"In iteration {j}.")
    costSum = 0
    savedStates = []
    completedPaths = []

    x = np.random.rand(9) * 10
    y = np.random.rand(9) * 10
    copyX = list(x)
    copyY = list(y)

    source_x = np.random.rand() * 10
    source_y = np.random.rand() * 10
    copySource_x = source_x
    copySource_y = source_y

    Path = []

    start = time.perf_counter()
    Path.append((copySource_x, copySource_y))
    for i in range(9):
        indx = calcCost(copySource_x, copySource_y, copyX, copyY)
        copySource_x = copyX.pop(indx)
        copySource_y = copyY.pop(indx)
        Path.append((copySource_x, copySource_y))
    timeTaken = time.perf_counter() - start
    unoptTime.append(timeTaken)
    unoptMinCosts.append(costSum)

    savedStates.append(savedState(x, y, (source_x, source_y), 0, [(float(source_x), float(source_y))])) #initializes the first saved state

    DEFAULT_TOLERANCE = 8
    optTolerances.append(DEFAULT_TOLERANCE)
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
    minPath = completedPaths[0]
    for path in completedPaths:
        if (path.cost < minPath.cost) : minPath = path
    timeTaken = time.perf_counter() - start
    optTime1.append(timeTaken)
    optMinCosts1.append(minPath.cost)

    savedStates = []
    completedPaths = []
    savedStates.append(savedState(x, y, (source_x, source_y), 0, [(float(source_x), float(source_y))])) #initializes the first saved state

    DEFAULT_TOLERANCE = 10
    optTolerances.append(DEFAULT_TOLERANCE)
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
    minPath = completedPaths[0]
    for path in completedPaths:
        if (path.cost < minPath.cost) : minPath = path
    timeTaken = time.perf_counter() - start
    optTime2.append(timeTaken)
    optMinCosts2.append(minPath.cost)

    savedStates = []
    completedPaths = []
    savedStates.append(savedState(x, y, (source_x, source_y), 0, [(float(source_x), float(source_y))])) #initializes the first saved state

    # DEFAULT_TOLERANCE = 2.065
    # optTolerances.append(DEFAULT_TOLERANCE)
    # start = time.perf_counter()
    # while True:
    #     currState = savedStates.pop()
    #     if (currState.toVisit):
    #         while currState.toVisit:
    #             visiting = currState.toVisit.pop()
    #             mask = ~((currState.X == visiting[0]) & (currState.Y == visiting[1]))
    #             savedStates.append(savedState(currState.X[mask], currState.Y[mask],
    #                                         (visiting[0], visiting[1]),
    #                                         currState.cost + ((currState.source[0] - visiting[0])**2 + (currState.source[1] - visiting[1])**2),
    #                                         currState.visited + [visiting],))
    #     else:
    #         completedPaths.append(currState)
    #     if not savedStates:
    #         break
    # minPath = completedPaths[0]
    # for path in completedPaths:
    #     if (path.cost < minPath.cost) : minPath = path
    # timeTaken = time.perf_counter() - start
    # optTime3.append(timeTaken)
    # optMinCosts3.append(minPath.cost)

    # savedStates = []
    # completedPaths = []
    # savedStates.append(savedState(x, y, (source_x, source_y), 0, [(float(source_x), float(source_y))])) #initializes the first saved state
    
    # DEFAULT_TOLERANCE = 2.1
    # optTolerances.append(DEFAULT_TOLERANCE)
    # start = time.perf_counter()
    # while True:
    #     currState = savedStates.pop()
    #     if (currState.toVisit):
    #         while currState.toVisit:
    #             visiting = currState.toVisit.pop()
    #             mask = ~((currState.X == visiting[0]) & (currState.Y == visiting[1]))
    #             savedStates.append(savedState(currState.X[mask], currState.Y[mask],
    #                                         (visiting[0], visiting[1]),
    #                                         currState.cost + ((currState.source[0] - visiting[0])**2 + (currState.source[1] - visiting[1])**2),
    #                                         currState.visited + [visiting],))
    #     else:
    #         completedPaths.append(currState)
    #     if not savedStates:
    #         break
    # minPath = completedPaths[0]
    # for path in completedPaths:
    #     if (path.cost < minPath.cost) : minPath = path
    # timeTaken = time.perf_counter() - start
    # optTime4.append(timeTaken)
    # optMinCosts4.append(minPath.cost)

xAxis = list(range(10))

axes[0].set_title("Minimum cost of each iteration:")
axes[0].plot(xAxis, unoptMinCosts, label = "unoptCost", color = "blue")
axes[0].plot(xAxis, optMinCosts1, label = "optCost - 8", color = "green")
axes[0].plot(xAxis, optMinCosts2, label = "optCost - 10", color = "orange")
# axes[0].plot(xAxis, optMinCosts3, label = "optCost - 2.065", color = "orange")
# axes[0].plot(xAxis, optMinCosts4, label = "optCost - 2.1", color = "red")
axes[0].legend(loc="best")
axes[0].set_ylabel("Distance^2")
axes[0].set_xlabel("Iterations")

axes[1].set_title("Time taken by each iteration:")
axes[1].plot(xAxis, unoptTime, label = "unoptCost", color = "blue")
axes[1].plot(xAxis, optTime1, label = "optTime - 8", color = "green")
axes[1].plot(xAxis, optTime2, label = "optTime - 10", color = "orange")
# axes[1].plot(xAxis, optTime3, label = "optTime - 2.065", color = "orange")
# axes[1].plot(xAxis, optTime4, label = "optTime - 2.1", color = "red")
axes[1].legend(loc="best")
axes[1].set_ylabel("Time taken (s)")
axes[1].set_xlabel("Iterations")

plt.show()