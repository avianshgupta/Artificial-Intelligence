import sys
import matplotlib.pyplot as plt
import random as rd
from copy import deepcopy
sys.path.append('..')
from utils import *

class Point: 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 

class Search_Space:
    def __init__(self,m,n):
        self.polys = []
        self.m = m
        self.n = n

    def remove_middle(self, a, b, c):
        cross = (a[0] - b[0]) * (c[1] - b[1]) - (a[1] - b[1]) * (c[0] - b[0])
        dot = (a[0] - b[0]) * (c[0] - b[0]) + (a[1] - b[1]) * (c[1] - b[1])
        return cross < 0 or cross == 0 and dot <= 0


    def convex_hull(self, points):
        '''
        Input: a list of points
        Output: convex hull for the given list off points
        '''
        spoints = sorted(points)
        hull = []
        for p in spoints + spoints[::-1]:
            while len(hull) >= 2 and self.remove_middle(hull[-2], hull[-1], p):
                hull.pop()
            hull.append(p)
        hull.pop()
        return hull

    def generate_state_space(self):
        '''
        Generates a 2D plane with polygons
        '''
        i = 0
        n = rd.randint(15,20)
        of = 200
        #if self.m == 1000:
        #    of = 250
        ct = 0
        while(i < self.m):
            j = 0
            while(j < self.n):
                pts = []
                for _ in range(n):
                    x,y = rd.randint(i,i+99),rd.randint(j,j+199)
                    pts.append((x,y))
                self.polys.append(self.convex_hull(pts))
                ct+=1
                j += of
            i += (of - 100)
        print('Number of Polygons: ',ct)
    
    def get_state_space(self):
        '''
        Input: 
        Output: list of polygons
        '''
        self.generate_state_space()
        return self.polys

class visibility_graph:
    def __init__(self, polys, start, goal):
        self.polys = polys
        self.start = start
        self.goal = goal

    def onSegment(self,p, q, r): 
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
            return True
        return False
    
    def orientation(self,p, q, r):       
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
        if (val > 0):   
            return 1
        elif (val < 0): 
            return 2
        else:
            return 0
    
    def doIntersect(self,p1,q1,p2,q2):  #source: Geeks for Geeks
        '''
        Input: 4 points representing two line segments
        Output: returns True if the two given lines intersect
        ''' 
        o1 = self.orientation(p1, q1, p2) 
        o2 = self.orientation(p1, q1, q2) 
        o3 = self.orientation(p2, q2, p1) 
        o4 = self.orientation(p2, q2, q1) 

        if ((o1 != o2) and (o3 != o4)): 
            return True
    
        if ((o1 == 0) and self.onSegment(p1, p2, q1)): 
            return True
    
        if ((o2 == 0) and self.onSegment(p1, q2, q1)): 
            return True
    
        if ((o3 == 0) and self.onSegment(p2, p1, q2)): 
            return True
    
        if ((o4 == 0) and self.onSegment(p2, q1, q2)): 
            return True
    
        return False

    def poly_edges(self):
        '''
        Input:
        Output: Returns a list of edges of all the polygons 
        '''
        edges = []
        for pol in self.polys:
            n = len(pol)
            for i in range(n):
                edges.append((pol[i],pol[(i + 1) % n]))
        return edges

    def get_poly_id(self,v):
        '''
        Input: a single vertex
        Output: id of polygon in which v is a vertex and its index
        '''
        for pid in range(len(self.polys)):
            if v in self.polys[pid]:
                return pid, self.polys[pid].index(v)

    def create_visibility_graph(self):
        '''
        Input: 
        Output: returns a graph of form {v1:{n1:c1, n2:c2}} where v1 is a vertex
                n1, n2 are its neighbours and c1, c2 are the cost corresponding to the
                edge v1n1, v1,n2 resp.
        '''
        V = []  # list of all the vertices
        V.append(self.start)
        for i in self.polys:
            for j in i:
                V.append(j)
        V.append(self.goal)
        edges = self.poly_edges()
        vg = {}     # visibility graph
        for v1 in V:
            vg[v1] = {}
            for v2 in V:
                if v1 != v2:
                    flag1 = 0
                    if ((v1 != self.start and v1 != self.goal) and (v2 != self.start and v2 != self.goal)):
                        pid1,i1 = self.get_poly_id(v1)
                        pid2,i2 = self.get_poly_id(v2)
                        n = len(self.polys[pid1])
                        flag1 = 1
                    if flag1 == 0 or (pid1 != pid2) or ((pid1 == pid2) and (v2 == self.polys[pid1][(i1+1)%n] or v2 == self.polys[pid1][(i1+n-1)%n])):
                        p1 = Point(v1[0],v1[1])
                        q1 = Point(v2[0],v2[1])
                        flag = 0
                        for e in edges:
                            if (v1 not in e) and (v2 not in e):
                                p2 = Point(e[0][0],e[0][1])
                                q2 = Point(e[1][0],e[1][1])
                                if self.doIntersect(p1,q1,p2,q2):
                                    flag = 1
                                    break
                        if flag == 0:
                            vg[v1][v2] = float('%.4f'%(euclidean_distance(v1,v2)))
        return vg
    

#polys = [[(0.0,1.0), (3.0,1.0), (1.5,4.0)],[(4.0,4.0), (7.0,4.0), (5.5,8.0)]]
#states = {'start':(1.5,0.0),'goal':(4.0, 6.0)}

#polys = [[(3.0,7.0),(7.0,9.6),(9.6,7.1),(4.5,4.0),(3.7,4.7)],[(4.3,2.8),(4.3,0.4),(15.0,0.5),(15.0,2.9)],[(11.1,7.6),(9.7,3.9),(12.5,3.9)],[(12.9,9.4),(12.9,6.4),(17.4,8.2),(15.5,9.6)],[(15.4,5.1),(16.6,1.6),(18.8,3.2)],[(17.9,9.3),(17.9,4.4),(22.4,4.4),(22.4,9.3)],[(20.5,2.9),(20.5,1.2),(22.6,0.3),(24.7,1.0),(24.7,2.9),(22.9,4.1)],[(23.0,8.7),(25.3,3.8),(25.9,8.5),(24.7,9.4)]]
#states = {'start':(3.2,1.6),'goal':(26.5,9.3)}

def get_SS():
    sel = rd.randint(1,2)
    if sel == 1:
        x,y = 500,1000
        states = {'start':(0.0,0.0),'goal':(500.0,1000.0)}
    else:
        x,y = 1000,1000
        states = {'start':(0.0,0.0),'goal':(1000.0,1000.0)}
    p = Search_Space(x,y)
    polys = p.get_state_space()
    return states,polys

