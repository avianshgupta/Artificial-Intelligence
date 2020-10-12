from helper import *
from generator import *
import time

import matplotlib.pyplot as plt

class GraphProblem(Problem):
    """The problem of searching a graph from one node to another."""

    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, A):
        """The actions at a graph node are just its neighbors."""
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        """The result of going to a neighbor is just that neighbor."""
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or np.inf)

    def find_min_edge(self):
        """Find minimum value of edges."""
        m = np.inf
        for d in self.graph.graph_dict.values():
            local_min = min(d.values())
            m = min(m, local_min)

        return m

    def h(self, node):
        """h function is straight-line distance from a node's state to goal."""
        locs = getattr(self.graph, 'locations', None)
        if locs:
            if type(node) is str:
                return int(distance(locs[node], locs[self.goal]))

            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return np.inf

class Analysis:
    def compare_searchers(self,problems, header,
                      searchers=[breadth_first_graph_search,
                                 depth_first_graph_search,
                                 greedy_best_first_graph_search,
                                 astar_search]):
        def do(searcher, problem):
            p = InstrumentedProblem(problem)
            bt = time.time()
            val = searcher(p)
            tt = time.time() - bt
            '''
            print('-------------------------------------------------------')
            print(name(searcher))
            print('Path: ',val.path())
            print('Total Cost: %.2f'%val.path_cost)
            print('-------------------------------------------------------')
            x,y = [],[]
            plotpath({'start':problem.graph.init,'goal':problem.graph.fin},visgh.poly_edges())
            for i in val.path():
                x.append(i.state[0])
                y.append(i.state[1])
            plt.title(name(searcher),loc='center')
            plt.plot(x,y,color='r')
            plt.show()'''
            return p,tt,val.path_cost

        table = []
        for s in searchers:
            avgstates,avgsucce,avggltest,avgtime,avgcost = 0,0,0,0,0
            for p in problems:
                sol = do(s,p)
                avgstates += sol[0].states
                avgsucce += sol[0].succs
                avggltest += sol[0].goal_tests
                avgtime += sol[1]
                avgcost += sol[2]
            
            print("\n",name(s))
            print("State: ", avgstates)
            print("Successors: ", avgsucce)
            print("Goal Tests: ", avggltest)
            print("Time: %.5f"%(avgtime))
            print("Cost: %.5f\n"%(avgcost))


    def compare_graph_searchers(self,problems):
        """Prints a table of search results."""
        self.compare_searchers(problems,
                        header=['Searcher', 'Successors\tGoal Tests\tStates\tGoal State','\tTime'])

def plotpath(states,edges,choice=1):
    plt.xlabel('x - axis') 
    plt.ylabel('y - axis')
    plt.text(states['start'][0],states['start'][1],'S',fontsize=12,color='r',horizontalalignment='right')
    plt.text(states['goal'][0],states['goal'][1],'G',fontsize=12,color='g',horizontalalignment='left')
    plt.scatter([states['start'][0],states['goal'][0]],[states['start'][1],states['goal'][1]],5,color='b')

    if choice == 1:
        for e in edges:
            x,y = [e[0][0],e[1][0]],[e[0][1],e[1][1]]
            plt.plot(x,y,color='k',marker='.',markersize=10,markerfacecolor='blue',linewidth=1)

    elif choice == 2:
        for i in g:
            for j in g[i].keys():
                plt.plot([i[0],j[0]],[i[1],j[1]],color='b',marker='.',markersize=10,markerfacecolor='k',linewidth=0.1)

    plt.scatter([states['start'][0]],[states['start'][1]],5,color='b',label='S({},{})'.format(states['start'][0],states['start'][1]))
    plt.scatter([states['goal'][0]],[states['goal'][1]],5,color='b',label='G({},{})'.format(states['goal'][0],states['goal'][1]))
    plt.legend(loc=4)   
    if choice == 2:
        plt.show()


all_graphs = []     # to store all the graphs
stfin = []          # to store start and goal state for all the graphs
alle = []           # to store the edges of all the polygons for all the graphs
bt = time.time()
for i in range(1):
    states,polys = get_SS()
    visgh = visibility_graph(polys,states['start'],states['goal'])
    alle.append(visgh.poly_edges())
    g = visgh.create_visibility_graph()
    all_graphs.append(g)
    stfin.append((states['start'],states['goal']))
print("Time taken to create Visibility Graphs: ",(time.time() - bt))

# Code used to plot the graphs
'''
plt.title('Visibility Graph',loc='center')
for edges in alle:
    for e in edges:
        x,y = [e[0][0],e[1][0]],[e[0][1],e[1][1]]
        plt.plot(x,y,color='k',marker='.',markersize=10,markerfacecolor='blue',linewidth=1)
    plt.text(states['start'][0],states['start'][1],'S',fontsize=12,color='r',horizontalalignment='right')
    plt.text(states['goal'][0],states['goal'][1],'G',fontsize=12,color='g',horizontalalignment='left')
    plt.scatter([states['start'][0]],[states['start'][1]],5,color='b',label='S({},{})'.format(states['start'][0],states['start'][1]))
    plt.scatter([states['goal'][0]],[states['goal'][1]],5,color='b',label='G({},{})'.format(states['goal'][0],states['goal'][1]))
    plt.legend(loc=4)
    plt.show()
ind = 0
for edges in alle:
    for e in edges:
        x,y = [e[0][0],e[1][0]],[e[0][1],e[1][1]]
        plt.plot(x,y,color='k',marker='.',markersize=10,markerfacecolor='blue',linewidth=1)
    plotpath({'start':stfin[ind][0],'goal':stfin[ind][1]},edges,2)
    plt.show()
'''

allg = []
ind = 0
for g in all_graphs:
    gph = UndirectedGraph(stfin[ind][0],stfin[ind][1],g)
    ind += 1
    gph.locations = {}
    for i in g:
        gph.locations[i] = i
    allg.append(gph)

ana = Analysis()
ana.compare_graph_searchers([GraphProblem(graph.init,graph.fin, graph) for graph in allg])
