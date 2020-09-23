# Sudoku Solver

## Sudoku Rules
  1. All the numbers should be in the range 1 to 9.
  2. All the numbers in a row must be unique.
  3. All the numbers in a column must be unique.
  4. All the numbers in the corresponding 3x3 must be unique.

## State Space Formulation
  1. **Initial State:** A partially filled 2d matrix representing a Sudoku puzzle(0 means empty cell).  
  2. **Actions:** Store all possible non conflicting values(according to the rules) in a list and return that.
  Eg. if for a cell if values 1, 3, 4, 6, 9 are already there in the respective row, column or 3x3 the list
  of possible values will be [2, 5, 7, 8].  
  3. **Goal Test:** If all the 81 cells are filled then return True else return False.  
  **Note:** No need to check if the solution is correct or not as all the values are filled only after
  checking for conflicts.  
  4. **Final State:** A fully filled 2d matrix representing a solved sudoku.  
  5. **Path Cost:** None (Our intention is not to find the path but to find the goal state).

## File Description
  1. [sudoku.py](https://github.com/avianshgupta/Artificial-Intelligence-Lab/blob/master/Sudoku_Solver/sudoku.py): It contains the implementation of the Problem abstract class and the Analysis class
  for the empirical analysis of the search strategies used.
  
  2. [helper.py](https://github.com/avianshgupta/Artificial-Intelligence-Lab/blob/master/Sudoku_Solver/helper.py): It contains the following:
   - Problem abstract class  
   - Node class for defining states.  
   - InstrumentedProblem class for analysis.  
   - Breadth First Search Implementation  
   - Depth First Search Implementation  
   - Depth Limit Search Implementation  
   - Iterative Deepening Search Implementation
  
  3. **instances.txt:** It contains a dictionary with various instances of sudoku separated by keys(easy,
  medium and hard).

## Search Strategies Used
 - Breadth First Search (BFS)
 - Depth First Search (DFS)
 - Depth Limit Search (DLS)
 - Iterative Deepening Search (IDS)

## Solving the instances using the basic search strategies
<img src="https://user-images.githubusercontent.com/45178946/93976851-3936c080-fd97-11ea-9fbb-d83f2b2805aa.png" alt="sudoku" width="350" />

<img src="https://user-images.githubusercontent.com/45178946/93976924-553a6200-fd97-11ea-81c3-3c54655a11b4.png" alt="bfs" width="350" /><img src="https://user-images.githubusercontent.com/45178946/93976975-6daa7c80-fd97-11ea-8c1a-8a99685445aa.png" alt="dfs" width="350" height="287" />
<img src="https://user-images.githubusercontent.com/45178946/93977027-80bd4c80-fd97-11ea-9a96-a5e82fe0e68e.png" alt="dls" width="350" /><img src="https://user-images.githubusercontent.com/45178946/93977042-887cf100-fd97-11ea-9180-5782dd60b401.png" alt="ids" width="350" height="309"/>

### Easy Instances
| Searcher | States Traversed | Successor States | Goal Tests | Time |
|---|---|---|---|---|
| BFS | 563 | 563 | 564 | 0.32195 |
| DFS | 321 | 314 | 315 | 0.17002 |
| DLS | 305 | 297 | 298 | 0.17026 |
| IDS | 18880 | 18357 | 18922 | 7.66987 |

### Medium Instances
| Searcher | States Traversed | Successor States | Goal Tests | Time |
|---|---|---|---|---|
| BFS | 115486 | 115486 | 115490 | 16.57369 |
| DFS | 71859 | 71845 | 71845 | 9.34528 |
| DLS | 43715 | 43698 | 43701 | 6.45239 |
| IDS | 3719482 | 3604031 | 3604020 | 619.726835 |

### Hard Instances
| Searcher | States Traversed | Successor States | Goal Tests | Time |
|---|---|---|---|---|
| BFS | 325546 | 325546 | 325546 | 85.44823 |
| DFS | 198646 | 198632 | 198632 | 46.374615 |
| DLS | 126987 | 126970 | 126970 | 30.342595 |
| IDS | - | - | - | - |

**Note:** The hard and medium instances were taken from a different dataset than that of the easy ones. IDS was taking very long to complete for the hard puzzles that’s why it's not included.

**Q. Is it possible to fix a reasonable limit a priori for Depth Limited Search?**  
For a given Sudoku matrix we can predict the limit for DLS by counting the total number of unfilled cells in our initial state.

## Ideas for going beyond basic search strategies
Since in the actions we are generating the number of possible values that can be placed in a cell so we can prioritize the filling of cells based on the minimum possible values i.e. Instead of choosing the first empty cell we can choose the cell having the minimum number of possible values that can be added to the cell. By choosing the cell with 2 possible values instead of 3 or 4 we can reduce the branching factor and hence solve the problem more efficiently.  
This idea can be implemented using a priority queue based on the number of possible values for a cell.
