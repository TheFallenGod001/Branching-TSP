# Branching-TSP

A comparison between plain greedy nearest-neighbor pathfinding and a **tolerance-pruned branching search** for approximating the Traveling Salesman Problem, with an empirical benchmark measuring both solution quality and runtime.

## The core idea

Greedy nearest-neighbor pathfinding always jumps to the single closest unvisited point. It's fast, but it's known to make locally-good decisions that lead to globally bad tours — committing early to a "closest" point can leave you stranded with long detours later.

This project explores a middle ground: instead of committing to only the single nearest point at each step, keep **every candidate within a tolerance factor of the nearest one**, and explore all of them as separate branches. Once a branch runs out of points, it's a completed candidate path. At the end, the completed path with the lowest total cost wins.

`tolerance` is the key dial:
- `tolerance ≈ 1` → collapses to plain greedy nearest-neighbor (only the single closest candidate survives the filter)
- Large `tolerance` → approaches exhaustive search over all point orderings, and the search tree grows exponentially

> **Note on naming:** despite the filename, this is **not** a guaranteed-optimal TSP solver. True branch-and-bound TSP relies on a mathematically justified lower bound (e.g. an MST-based bound) to *prove* a branch can't beat the current best before discarding it. This algorithm prunes using a tunable distance-ratio heuristic instead, which is effective but can still discard the true optimal path if it doesn't look locally competitive at some step. It's more accurately described as a **tolerance-pruned branching / bounded beam search** than an optimal solver.

## Files

```
Branching-TSP/
├── unoptimizedPathFinding.py   # Plain greedy nearest-neighbor baseline, standalone demo
├── optimal path.py             # Side-by-side demo: greedy vs. branching search, same point set
└── pathingBenchmark.py         # Empirical benchmark across multiple tolerance values, 10 trials
```

## How the branching search works (`savedState`)

Each `savedState` represents one partially-built path:

- The remaining unvisited points (`X`, `Y`)
- The current position (`source`)
- The cumulative cost so far (`cost`)
- The path taken to get here (`visited`)

On creation, it scans the remaining points, finds the nearest one, and keeps every point within `tolerance × nearestCost` as a candidate (`toVisit`) to branch into next.

The main loop is an explicit stack-based DFS: pop a state, branch into every one of its `toVisit` candidates (pushing a new `savedState` for each), and repeat until every branch has been fully explored. All fully-explored (leaf) states are collected, and the lowest-cost one is the answer.

## Benchmark methodology (`pathingBenchmark.py`)

For 10 randomized trials (9 points each):
1. Run the plain greedy baseline, record its total cost and time
2. Run the branching search at `tolerance = 8`, record cost and time
3. Run the branching search at `tolerance = 10`, record cost and time
4. Plot cost and time for all three across all 10 trials

This gives a real cost/speed tradeoff comparison rather than a single anecdotal result — costs are consistently measured in squared distance throughout (avoiding unnecessary `sqrt` calls, since argmin is unaffected by that monotonic transform).

## Running

```bash
python "unoptimizedPathFinding.py"   # Greedy baseline only, 19 points, animated arrows
python "optimal path.py"             # Greedy vs. branching search, side-by-side plot, 19 points
python pathingBenchmark.py           # Full benchmark: cost & time across tolerances, 10 trials
```

Requires `matplotlib` and `numpy`.

## Known issues / fragility

- Branches identify "the point just visited" via **exact float equality** (`currState.X == visiting[0]`). This works because coordinates are only ever copied, never recomputed, so bit-for-bit equality holds in practice — but it's inherently fragile if two points ever land on identical coordinates.
- The branching search's runtime grows quickly with both node count and `tolerance` — the benchmark tests only 9 points for the branching search vs. 19 for the plain greedy demo, likely for exactly this reason.

## Roadmap

- [ ] Replace float-equality point matching with index-based tracking, to remove the fragility around duplicate coordinates
- [ ] Test at higher node counts to characterize how tolerance vs. runtime actually scales
