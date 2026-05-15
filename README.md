# Branching TSP

Trying out a different way of doing TSP, and seeing how it stacks up against the usual greedy nearest-neighbor heuristic.

## The idea

Greedy nearest neighbor is the standard cheap-and-cheerful TSP heuristic: at every step, go to the closest unvisited point. It runs fast, it's easy, and it gets trapped easily. Once it commits to a near point, there's no going back, and that one commitment can cost you the rest of the tour.

The approach in `optimal path.py` softens that. Instead of always picking *the* nearest point, it picks *every* point that's "close enough" to the nearest one and explores all of those as separate branches. "Close enough" is controlled by a single knob:

```
tolerance = 1.0   →   pure greedy
tolerance = 2.0   →   also explore any point up to 2× the nearest squared distance
tolerance = 5.0   →   wider still
```

Each branch runs all the way to a complete tour, and the cheapest one wins. So instead of one path, you generate a tree of partial paths and let the structure of the problem decide where it's worth spreading out.

It's basically depth-first beam search where the beam width is decided dynamically at every node by the cost-ratio threshold, rather than being a fixed number.

All costs are summed squared distance, no sqrt. Cheaper to compute and orders paths the same way for picking the minimum.

## Files

`optimal path.py` is the main thing. It builds a random 20-node graph, runs both the branching search and plain greedy on it, and plots both tours side by side so you can see where the branching version actually does something different.

`unoptimizedPathFinding.py` is the plain greedy version on its own, with the matplotlib viz. Useful as a sanity-check starting point. This is also the reference algorithm the new approach is being compared against.

`pathingBenchmarkl.py` runs both approaches 10 times on fresh random graphs and plots cost and runtime per iteration, for a couple of tolerance values. This is where you go to see whether the extra work is actually buying you better tours, and how much it costs you in time.

## Running it

```
pip install numpy matplotlib
python "optimal path.py"
```

(The space in the filename needs quotes from the shell. Or rename it to `optimal_path.py` and move on with your life.)

## How `savedState` works

This class is the workhorse of the branching search. Each instance is a snapshot of one partial tour:

* `X`, `Y` are the still-unvisited points
* `source` is where the agent currently sits
* `cost` is the accumulated squared distance so far
* `visited` is the ordered list of points already taken
* `toVisit` is the candidates that the search is allowed to branch into from `source`

When `scan()` runs, it computes squared distances from `source` to every unvisited point, finds the minimum, and keeps everything within `min_cost * tolerance` of it. Those become the branch candidates.

The main loop pops a state off the stack, branches it into children (one new `savedState` per candidate), and pushes the children back on. If a state has no candidates left, that path is done and gets dropped into `completedPaths`. When the stack empties, the run is over and you scan `completedPaths` for the cheapest one.

## Notes

The benchmark currently runs tolerances of 8 and 10 (two more blocks at 2.065 and 2.1 are commented out). On 9-node graphs at tolerance 10 you're already generating a lot of states, so don't crank it higher without watching memory.

`DEFAULT_TOLERANCE = 5` in `optimal path.py` is reasonable for 20 nodes. Past about 6 or 7 the runtime climbs sharply.

Squared distance is the cost everywhere. If you want real Euclidean tour length, sqrt each leg before summing. The branching itself doesn't care about the metric as long as it's monotonic in distance, but if you compare costs across algorithms keep them using the same one.

The mask in the main loop assumes no duplicate point coordinates. With random floats that's effectively always true, but with real data containing overlapping points it would need to use indices instead of value comparison.

## Possible next steps

* Memoize on (visited set, current source) so identical subproblems don't get re-explored
* Best-first ordering of the stack so high-promise paths finish first and bound the rest
* A real lower bound (MST, 1-tree) to prune branches that can't beat the current best completed tour
* Replace the linear `calcCost` scan with a kdtree for larger node counts
* Make the tolerance shrink with depth — early decisions matter more, so let them branch wider
