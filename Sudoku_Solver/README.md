# Sudoku Solver

### Sudoku Rules
  1. All the numbers should be in the range 1 to 9.
  2. All the numbers in a row must be unique.
  3. All the numbers in a column must be unique.
  4. All the numbers in the corresponding 3x3 must be unique.

### State Space Formulation
  1. **Initial State:** A partially filled 2d matrix representing a Sudoku puzzle(0 means empty cell).  
  2. **Actions:** Store all possible non conflicting values(according to the rules) in a list and return that.
  Eg. if for a cell if values 1, 3, 4, 6, 9 are already there in the respective row, column or 3x3 the list
  of possible values will be [2, 5, 7, 8].  
  3. **Goal Test:** If all the 81 cells are filled then return True else return False.  
  **Note:** No need to check if the solution is correct or not as all the values are filled only after
  checking for conflicts.  
  4. **Final State:** A fully filled 2d matrix representing a solved sudoku.  
  5. **Path Cost:** None (Our intention is not to find the path but to find the goal state).

### File Description
  1. **sudoku.py:** It contains the implementation of the Problem abstract class and the Analysis class
  for the empirical analysis of the search strategies used.
  
  2. **helper.py:** It contains the following:
   - Problem abstract class  
   - Node class for defining states.  
   - InstrumentedProblem class for analysis.  
   - Breadth First Search Implementation  
   - Depth First Search Implementation  
   - Depth Limit Search Implementation  
   - Iterative Deepening Search Implementation
  
  3. **instances.txt:** It contains a dictionary with various instances of sudoku separated by keys(easy,
  medium and hard).

### Search Strategies Used
  1. Breadth First Search (BFS)
  2. Depth First Search (DFS)
  3. Depth Limit Search (DLS)
  4. Iterative Deepening Search (IDS)
