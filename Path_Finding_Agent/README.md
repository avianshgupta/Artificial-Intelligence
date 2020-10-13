# Path Finding Agent
## Problem Statement
Consider an autonomous mobile robot in a crowded environment that needs to find an efficient
path from its current location S to a desired location G. As an idealization of the situation,
assume that the obstacles (whatever they may be) are abstracted by polygons. The problem now
reduces to finding the shortest path between two points in a plane that has convex polygonal
obstacles.
![image](https://user-images.githubusercontent.com/45178946/95865680-91ecee00-0d84-11eb-9f78-52d9c5dd573e.png)

## State Space Formulation
Since, the state space is continuous so there are infinitely many states possible and as a result infinitely
many paths to the goal state.  
For this problem, we can consider the start and goal point to be vertices.  
We know that,  
The shortest distance between two points is a straight line, and if it is not possible to travel in a straight
line because some obstacle is in the way, then the next shortest distance is a sequence of line segments,
end-to-end, that deviate from the straight line as little as possible. So the first segment of this sequence
must go from the start point to a tangent point on an obstacle - any path that gives the polygon a wider
girth would be longer. Because the obstacles are polygons, the tangent point must be vertices of the
obstacles and hence the entire path must go from vertex to vertex. So now the state space is the set of
vertices, of which there are 35 in the above figure.
  1. **Initial State:** Start vertex (S)
  2. **Actions:** It will return all the possible successors of the current state. Successors of the current
  state will be all the vertices that can be connected to the current state with a straight line without
  any intersection with any of the edges of the polygons.
  3. **Goal Test:** If the value of heuristic of that state is zero then it’s the goal state.
  4. **Final State:** Goal vertex (G)
  5. **Path Cost:** Sum of euclidean distance between all the points in the path from start state to the
  goal.
  6. **Heuristic Function:** Here straight line distance between the start state and the goal state is used
  as heuristic.
  
## File Description
1. [pathfinding.py](https://github.com/avianshgupta/Artificial-Intelligence/blob/master/Path_Finding_Agent/pathfinding.py): It contains the implementation of the Problem abstract class and the Analysis class for the empirical analysis of the search strategies used.
2. [helper.py](https://github.com/avianshgupta/Artificial-Intelligence/blob/master/Path_Finding_Agent/helper.py): It contains the following:
  - Problem abstract class
  - Node class for defining states.
  - Graph class for creating a graph.
  - InstrumentedProblem class for analysis.
  - Breadth First Search Implementation
  - Depth First Search Implementation
  - Greedy Best First Search
  - A* Search
3. [generator.py](https://github.com/avianshgupta/Artificial-Intelligence/blob/master/Path_Finding_Agent/generator.py): It contains the following:
  - Point class
  - Search Space class with the following functions:
    - generate_state_space: used for generating state space with polygon obstacles.
    - convex_hull: used to generate a polygon from a given set of points.
    - remove_middle: a utility function for convex_hull.
  Polygons are created by generating a random MxN grid and then dividing it into some
  small grids and then generating some random points in that respective grid. After that just
  generate the convex hull for that set of points which will give a polygon.
  - visibility_graph class with the following functions:
    - poly_edges: returns a list of edges of all the polygons.
    - Get_poly_id: returns id of polygon in which v is a vertex and its index.
    - create_visibility_graph: returns a graph of form {v1:{n1:c1, n2:c2}} where v1 is
    a vertex n1, n2 are its neighbours and c1, c2 are the cost corresponding to the
    edge v1n1, v1,n2 resp.
    - dointersect: returns true if two line segments are intersecting.
    
**Note:** A naive O(n^3) algorithm was used to create [visibility graph](https://en.wikipedia.org/wiki/Visibility_graph). Faster solutions are also available.
[Visibility Graph Algorithms](https://www.cs.unm.edu/~moore/tr/03-05/Kitzingerthesis.pdf)

## Algorithms Used
- Breadth First Search (BFS)
- Depth First Search (DFS)
- Greedy Best First Search
- A* Search

## Examples
**Instance 1**  
<img src="https://user-images.githubusercontent.com/45178946/95869184-be0a6e00-0d88-11eb-9791-829df07dca84.png" alt="instance" width="450" /><img src="https://user-images.githubusercontent.com/45178946/95869280-d5495b80-0d88-11eb-8f55-baa3e345bf81.png" alt="visgraph" width="450" />
<img src="https://user-images.githubusercontent.com/45178946/95869320-de3a2d00-0d88-11eb-9263-69e5f4e3d531.png" alt="bfs" width="450" /><img src="https://user-images.githubusercontent.com/45178946/95869365-e85c2b80-0d88-11eb-8c07-e7202db8af71.png" alt="dfs" width="450" />
<img src="https://user-images.githubusercontent.com/45178946/95869387-ee520c80-0d88-11eb-929c-6b4ad8e6e8c1.png" alt="bestfs" width="450" /><img src="https://user-images.githubusercontent.com/45178946/95869412-f447ed80-0d88-11eb-8902-b1f1ed4e1c9c.png" alt="astar" width="450" />
<img src="https://user-images.githubusercontent.com/45178946/95869452-fd38bf00-0d88-11eb-89a9-097b56992870.png" alt="results" width="450" />

**Instance 2**  
<img src="https://user-images.githubusercontent.com/45178946/95871528-602b5580-0d8b-11eb-804f-37cab02c8db1.png" alt="instance" width="450" /><img src="https://user-images.githubusercontent.com/45178946/95871553-68839080-0d8b-11eb-8f16-264f29c4379b.png" alt="visgraph" width="450" />
<img src="https://user-images.githubusercontent.com/45178946/95871577-70433500-0d8b-11eb-9680-ad75b56c8da5.png" alt="bfs" width="450" /><img src="https://user-images.githubusercontent.com/45178946/95871594-76d1ac80-0d8b-11eb-8687-ec160ca612d0.png" alt="dfs" width="450" />
<img src="https://user-images.githubusercontent.com/45178946/95871616-7d602400-0d8b-11eb-96d6-1a22f6ff8949.png" alt="bestfs" width="450" /><img src="https://user-images.githubusercontent.com/45178946/95871635-82bd6e80-0d8b-11eb-8d54-61d4d6a4272d.png" alt="astar" width="450" />
<img src="https://user-images.githubusercontent.com/45178946/95871681-8c46d680-0d8b-11eb-8cca-7920fe21eedc.png" alt="results" width="450" />

## For 100 Instances
Average time taken to create **visibility graphs** : 20.0849s
| Searcher | States Traversed | Successor States | Goal Tests | Time | Cost |
|---|---|---|---|---|---|
| BFS | 1371 | 85 | 165 | 0.01303 | 1704.672 |
| DFS | 119 | 9 | 10 | 0.00141 | 1917.033 |
| Greedy Best First Search | 61 | 5 | 6 | 0.00142 | 1720.597 |
| A* Search | 1247 | 73 | 74 | 0.08892 | 1343.324 |

**Note:** All the instances used have 25 to 30 polygons. An instance with 50 polygons takes 80 - 100s to generate the visibility graph.

# Conclusions
- **Path Cost:** A* search returns the optimal path with minimum path cost but it takes more time to find the path as compared to other algorithms.
- **Time:** DFS and Greedy takes the least amount of time as in greedy it chooses the nodes which
are closest to the goal state and as a result it traverses very less number of states and DFS
does not consider the path cost. But both of these algorithms return paths with a very high
cost.
