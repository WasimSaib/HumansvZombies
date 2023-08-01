from Node import Node
from heapq import heappop, heappush
from math import inf, sqrt

class Graph:
    def __init__(self, rows, cols, world, bidirectional = True):
        self._graph =  {}
        self._bidirectional = bidirectional
        self.maxRows = rows
        self.maxCols = cols
        self._world = world
        self.makeGraph()

    def makeGraph(self):
        self.add_nodes()
        self.add_arcs()

    def updateGraph(self):
        #this updates the graph in event of movement
        for r in range(self.maxRows):
            for c in range(self.maxCols):
                w = self._world[r][c] #new val
                n = self.findNode(r,c)
                if w != n._entity:
                    self.updateNodeValue(r,c,w) #update the entity value
    def add_nodes(self):
    #making each cell in the grid a node 
        for w in range(self.maxRows):
            for s in range(self.maxCols):
                n = Node(self._world[w][s], w, s) 
                self._graph[n._value] = n 
         
    def add_arc(self, src_node, des_node):
        self._graph[src_node._value].add_arc(des_node, 1)
        self._graph[des_node._value].add_arc(src_node, 1)
    def add_arcs(self):
        for key in self._graph:
            rr = self._graph[key]._value[0]
            cc = self._graph[key]._value[1]
            # refactor the code below
  
            # connect to row above
            if (rr - 1 >= 0 and rr - 1 <= self.maxRows): 
                self.connectNodes(rr-1, cc, self._graph[key])
            # connect to row below
            if (rr + 1 >= 0 and rr + 1 <= self.maxRows):
                self.connectNodes(rr+1, cc, self._graph[key])
            #connect to left node
            if(cc - 1 >= 0 and cc -1 <= self.maxCols):
                self.connectNodes(rr,cc-1, self._graph[key])
            # connect to right node
            if(cc + 1 >= 0 and cc + 1 <= self.maxCols):
                self.connectNodes(rr, cc+1, self._graph[key])
            #connect top right node
            if((rr - 1 >= 0 and rr - 1 <= self.maxRows) and (cc - 1 >= 0 and cc -1 <= self.maxCols)):
                self.connectNodes(rr-1, cc-1, self._graph[key])
            # connect top left node
            if((rr - 1 >= 0 and rr - 1 <= self.maxRows) and (cc - 1 >= 0 and cc -1 <= self.maxCols)):
                self.connectNodes(rr-1, cc + 1, self._graph[key])
            # connect down left
            if ((rr + 1 >= 0 and rr + 1 <= self.maxRows) and (cc - 1 >= 0 and cc -1 <= self.maxCols)):
                self.connectNodes(rr+1, cc-1, self._graph[key])    
            # connect down right
            if ((rr + 1 >= 0 and rr + 1 <= self.maxRows) and (cc + 1 >= 0 and cc + 1 <= self.maxCols)):
                self.connectNodes(rr+1, cc+1, self._graph[key])


    def ZombieBFS(self,start_vertex: Node, target_value:Node):
        path = [start_vertex] #The starting node
        vertex_path = [start_vertex, path] # the path of this traversal
        bfs_queue = [vertex_path]
        visited = set()
        while bfs_queue:
            current_vertex, path = bfs_queue.pop(0) # pop the first element of the path
            visited.add(current_vertex)
            for n in self._graph[current_vertex.get_value()]:
                if n._entity == 0 or n._entity == 1: #if there is space or a human
                    if n not in visited:
                        if n is target_value:
                            return path + [n]
                        else:
                            bfs_queue.append([n, path + [n]])

    def HumanBFS(self,start_vertex: Node, target_value:Node):
        path = [start_vertex] #The starting node
        vertex_path = [start_vertex, path] # the path of this traversal
        bfs_queue = [vertex_path]
        visited = set()
        while bfs_queue:
            current_vertex, path = bfs_queue.pop(0) # pop the first element of the path
            visited.add(current_vertex)
            for n in self._graph[current_vertex.get_value()]:
                if n._entity == 0 or n._entity == 3: #if there is space or the goal
                    if n not in visited:
                        if n is target_value:
                            return path + [n]
                        else:
                            bfs_queue.append([n, path + [n]])


    # def a_star(self, start, target):
    #     count = 0
    #     paths_and_distances = {}
    #     for vertex in self._graph:
    #         paths_and_distances[vertex] = [inf, [start._value]]
  
    #     paths_and_distances[start][0] = 0
    #     vertices_to_explore = [(0, start)]
    #     while vertices_to_explore and paths_and_distances[target][0] == inf:
    #         current_distance, current_vertex = heappop(vertices_to_explore)
    #     for neighbor, edge_weight in self._graph[current_vertex]:
    #         new_distance = current_distance + edge_weight + self.heuristic(neighbor._value, target._value)
    #         new_path = paths_and_distances[current_vertex][1] + [neighbor._value]
      
    #     if new_distance < paths_and_distances[neighbor][0]:
    #         paths_and_distances[neighbor][0] = new_distance
    #         paths_and_distances[neighbor][1] = new_path
    #         count += 1
    #         print("\nAt " + vertices_to_explore[0][1]._value)
        
  
    #     return paths_and_distances[target][1]


    def connectNodes(self, r:int, c:int, graph_n):
        #we check to see if the node is in the graph
        u = self.findNode(r,c)
        if u is not None:
            self.add_arc(graph_n, u)

    def findNode(self, r:int, c:int) -> Node:
        for key in self._graph:
            if key[0] == r and key[1] == c:
                return self._graph[(r,c)]

    def updateNodeValue(self, r, c,v):
        #we check to see if the node is in the graph
        n = self.findNode(r,c)
        if n is not None:
            n.updateNodeEntity(v)


          
    def findHumans(self):
        humans = []
        for n in range(self.maxRows):
            for k in range(self.maxCols):
                    # if we searching for humans
                    if self._world[n][k] == 1:
                        humans.append(self.findNode(n,k)) 
                    
        return humans

    def findSwitch(self):
        for w in range(self.maxRows):
            for s in range(self.maxCols):
                if self._world[w][s] == 3:
                    return self.findNode(w,s)
                
    def heuristic(self, start_loc:tuple, end_loc:tuple):
        # we make use of the distance formula:
        # distance = sqrt(abs((x2-x1))^2+abs((y2 - yl))^2) abs so we dont get negatives
        x = abs(start_loc[0] - end_loc[0]) 
        y = abs(start_loc[1] - end_loc[1])
        return (x**2 + y**2)**0.5