from helper import *
from copy import deepcopy
import time,json

class sudokusolver(Problem):
    def _init_(self,instance):
        super().__init__(instance)

    def find_unfilled_cell(self,state):
        row,col = -1,-1
        for i in range(len(self.initial)):
            for j in range(len(self.initial[0])):
                if state[i][j] == 0:
                    row,col = i,j
                    break
        return row,col
    
    def no_conflict(self,state,r,c,n):
        for i in range(len(state[0])):
            if i != c and state[r][i] == n:
                return False
        for i in range(len(state)):
            if i != r and state[i][c] == n:
                return False
        sr = (r//3)*3
        sc = (c//3)*3
        for i in range(sr,sr+3):
            for j in range(sc,sc+3):
                if (i != r and j != c) and state[i][j] == n:
                    return False
        return True
    
    def actions(self, state):
        row,col = self.find_unfilled_cell(state)
        possible_vals = []
        for n in range(1,10):
            if self.no_conflict(state,row,col,n):
                possible_vals.append(n)
        return possible_vals

    def goal_test(self, state):
        row,col = self.find_unfilled_cell(state)
        if row != -1 and col != -1:
            return False
        return True

    def result(self, state,action):
        row,col = self.find_unfilled_cell(state)
        next_state = deepcopy(state)
        next_state[row][col] = action
        return next_state
    
    def print_sudoku(self,state):
        print("+" + "---+"*9)
        for i, row in enumerate(state):
            print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
            if i % 3 == 2:
                print("+" + "---+"*9)

'''
sud = [[2, 0, 4, 0, 0, 0, 0, 0, 9],
       [0, 0, 6, 0, 0, 0, 1, 0, 4],
       [0, 8, 0, 7, 0, 0, 0, 2, 3],
       [0, 2, 0, 4, 8, 5, 9, 0, 6],
       [0, 5, 9, 2, 3, 0, 0, 0, 7],
       [0, 0, 8, 6, 7, 9, 5, 1, 2],
       [0, 1, 3, 8, 0, 7, 2, 0, 5],
       [0, 0, 5, 9, 1, 0, 0, 7, 8],
       [8, 0, 0, 5, 6, 3, 4, 0, 1]]


sud = [[5, 0, 0, 0, 0, 0, 0, 8, 0],
       [0, 0, 6, 3, 1, 0, 7, 5, 0],
       [1, 0, 0, 7, 0, 0, 0, 9, 0],
       [0, 0, 0, 0, 0, 6, 0, 7, 0],
       [0, 7, 9, 0, 0, 0, 2, 6, 0],
       [0, 5, 0, 8, 0, 0, 0, 0, 0],
       [0, 1, 0, 0, 0, 9, 0, 0, 7],
       [0, 8, 2, 0, 3, 4, 6, 0, 0],
       [0, 6, 0, 0, 0, 0, 0, 0, 3]]'''

class Analysis:
    def compare_searchers(self,problems, header,
                        searchers=[breadth_first_tree_search,
                                    depth_first_tree_search,
                                    depth_limited_search,
                                    iterative_deepening_search]):
        def do(searcher, problem):
            p = InstrumentedProblem(problem)
            #print(name(searcher))
            bf = time.time()
            ans = searcher(p)
            ft = time.time() - bf
            #problem.print_sudoku(ans.state)
            #sols.append(ans.state)
            return p,ft

        for s in searchers:
            avgstates,avgsucce,avggltest,avgtime = 0,0,0,0
            for p in problems:
                sol = do(s,p)
                avgstates += sol[0].states
                avgsucce += sol[0].succs
                avggltest += sol[0].goal_tests
                avgtime += sol[1]
            
            print("\n",name(s))
            print("State: ", avgstates // 35)
            print("Successors: ", avgsucce // 35)
            print("Goal Tests: ", avggltest // 35)
            print("Time: %.5f\n"%(avgtime / 35))
            '''
            print("\n",name(s))
            print("State: ", avgstates)
            print("Successors: ", avgsucce)
            print("Goal Tests: ", avggltest)
            print("Time: %.5f\n"%(avgtime))'''
    def compare_sudoku_searchers(self,problems):
        """Prints a table of search results."""
        
        self.compare_searchers(problems,
                        header=['Searcher', 'Total_States\tSuccessors\tGoal_Tests','Time Taken'])


def formatsudoku(l):
    new = []
    tmp = []
    for i in range(81):
        tmp.append(l[i])
        if i % 9 == 8:
            new.append(tmp)
            tmp = []
    return new

d = {}
sudoku_file = open('instances.txt','r')
instances = sudoku_file.read()
d = json.loads(instances)
ana = Analysis()

print("Easy puzzles ",len(d['easy']))
ana.compare_sudoku_searchers([sudokusolver(formatsudoku(i)) for i in d['easy']])
print("--------------------------------------------------------------------")
print("Medium puzzles ",len(d['medium']))
ana.compare_sudoku_searchers([sudokusolver(formatsudoku(i)) for i in d['medium']])
print("--------------------------------------------------------------------")
print("hard puzzles ",len(d['hard']))
ana.compare_sudoku_searchers([sudokusolver(formatsudoku(i)) for i in d['hard']])
print("--------------------------------------------------------------------")
