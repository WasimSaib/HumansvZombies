class Node:
    def __init__(self, value, row, col):
        self._value = (row, col) 
        self._entity = value #the value of the entity in the node at a given moment
        self._arcs = {} #list of joined arcs/edges

    def updateNodeEntity(self,v:int):
        self._entity = v


    def get_value(self):
        return self._value 
        
    def add_arc(self, node, weight=0):
        self._arcs[node] = weight
    
    def get_arcs(self):
        return list(self._arcs.keys())
    
    def __repr__(self) -> str:
        # return "("++")"
        return str(self._value)
    
    def __iter__(self):
        self._index = 0
        self._nodes = list(self._arcs.keys())
        return self
    
    def __next__(self):
        if self._index < len(self._nodes):
            result = self._nodes[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration
