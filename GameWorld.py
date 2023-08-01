import os 
import random 
import time
from GameAgent import GameAgent
from Human import Human
from Zombies import Zombie
from Graph import Graph

class World:
    def __init__(self, rows, cols, hums, zums):
        # Initial Values
        self._rows = rows
        self._cols = cols
        self._hums = hums
        self._zums = zums
        # Store entity objects
        self._aList = []
        self._humanDead = []
        self._aDict = {} #Key: Turn Value: List of Agent objects
        self._turns = 1 #track the turns
        self._world = [[0 for row in range(rows)] for col in range(cols)] 
        self._sprites = ['.','H', 'Z', 'S']
        self._state = True # the world is active
        self.initWorld() # Initialize the world
        self._graph = Graph(self._rows, self._cols, self._world)#init graph
    
    def initWorld(self):
        # Place the entities
        for w in range(self._hums):
            self.PlaceEntity(1)
        for s in range(self._zums):
            self.PlaceEntity(2)
        # Place the switch
        self.PlaceEntity(3)

    def showWorld(self):
        for w in range(self._rows):
            for s in range(self._cols):
                intEntity = self._world[w][s]
                print(self._sprites[intEntity] , end= ' ')
            print()
    
        
    def countEntity(self, entity_val):
        # count the entity
        count = 0
        for w in range(self._rows):
            for s in range(self._cols):
                if self._world[w][s] == entity_val:
                    count += 1
        return count
    
    def countAgent(self):
        count = 0
        for n in range(self._rows):
            for k in range(self._cols):
                if self._world[n][k] == 1 or self._world[n][k] == 2:
                    count += 1
        return count

    def PlaceEntity(self, entity):
    # generating random rows and colum to place
        randomRow = random.randint(0, self._rows - 1)
        randomCol = random.randint(0, self._cols - 1)

        if self.findEmptySpace(randomRow, randomCol) is True:
            # places the human in the cols of 0, 1, 2
            if entity == 1 and((randomCol <= 2) and self.countEntity(entity) <= self._hums) :
                self._world[randomRow][randomCol] = entity
                # self._ent[self._sprites[entity]] = (randomRow, randomCol)
                self._aList.append(Human(randomRow, randomCol))
            # places the zombie in the cols of 7, 8, 9
            elif entity == 2 and (randomCol >= 7 and self.countEntity(entity) <= self._zums):
                self._world[randomRow][randomCol] = entity
                self._aList.append(Zombie(randomRow, randomCol))
            elif entity == 3 and randomCol == 9 and self.countEntity(entity) <= 1:
                self._world[randomRow][randomCol] = entity
            else:
                return self.PlaceEntity(entity)
        else:
            return self.PlaceEntity(entity)
    
    def simulateGame(self):
        self.showWorld()
        while self._state == True:
            print("Humans Alive:" + str(self.countEntity(1)))
            for a in self._aList:
                self.moveAgents(a)
                # index of object 
                index = self._aList.index(a)
                # update the object on the list
                self._aList[index] = a 
                time.sleep(2)
                os.system("cls")
                self.showWorld()
            self._turns += 1
    
    def moveAgents(self, a:GameAgent):
        # Gets current location of agent
        cr, cc = a._currentLoc[0], a._currentLoc[1]
        start_location = self._graph.findNode(cr, cc)
        if a._type == 'H' and a._turn == self._turns - 1 and a._state == True:
            #goal node
            goal = self._graph.findSwitch()
            path = self._graph.HumanBFS(start_location, goal)
            # path = self._graph.a_star(start_location, goal)
            if path is not None:
                nr,nc = path[1]._value[0], path[1]._value[1]
                gr, gc = goal._value[0], goal._value[1] #switch_loc
                if nr == gr and nc == gc:
                    self._world[cr][cc] = 0
                    self._world[nr][nc] = a._value
                    self._graph.updateGraph()
                    a.updateTurn()
                    a.updateLoc(nr, nc)
                    # os.system('pause')
                    self._state = False
                    print("HUMANS WIN") 
                else:
                    # first update the old location to space
                    self._world[cr][cc] = 0
                    self._world[nr][nc] = a._value #move the entity
                    self._graph.updateGraph()
                    a.updateTurn()
                    a.updateLoc(nr, nc)
            else:
                # dont move -- stay where they are 
                a.updateTurn()
        elif a._type == 'Z' and a._turn == self._turns - 1:
            if self.countHumans() is True: #check if there are humans on the map
                human_list = self.findHumans() #return a list of human objects
                human_distance = {} #Key: the distance between zombie and human; value: the human object
                for h in human_list:
                    human_distance[self.heuristic(a._currentLoc, h._currentLoc)] = h
                #the closest human    
                closest_human = human_distance[min(human_distance.keys())]
                # convert human obbj to node for traversal.
                ch_node = self._graph.findNode(closest_human._currentLoc[0], closest_human._currentLoc[1])
                hr,hc = ch_node._value[0], ch_node._value[1] # location of nearest human
               
                path = self._graph.ZombieBFS(start_location, ch_node)
                if path is not None:
                    nr,nc = path[1]._value[0], path[1]._value[1]
                
                    if nr == hr and nc == hc:
                        self._world[cr][cc] = 0
                        self._world[nr][nc] = a._value
                    # set the state of the agent to false
                        for a in self._aList:
                            if a._currentLoc[0] == nr  and a._currentLoc[1] == nc:
                                self._aList.remove(a)
                    # find the index of the object
                    # index = self._aList.index(closest_human)
                    # self._aList.remove(self._aList(index))
                        self._graph.updateGraph()
                        a.updateTurn()
                        a.updateLoc(nr, nc)
                    
                    
                        # self._state = False #End the game

                    else:
                    # space goes in the old location
                        self._world[cr][cc] = 0
                        self._world[nr][nc] = a._value
                        self._graph.updateGraph()
                        a.updateTurn()
                        a.updateLoc(nr, nc)
                else:                
                     # dont move -- stay where they are 
                    a.updateTurn()

            else:
                self._state = False
                print("Zombies Win")
    def findHumans(self):
        humans = []
        for i in range(self._rows):
            for j in range(self._cols):
                if self._world[i][j] == 1:
                    humans.append(Human(i,j))
        return humans 
        
    def findEmptySpace(self, row, col):
        if self._world[row][col] == 0:
            return True
        else:
            return False
    
    def countHumans(self) -> bool:
        return self.countEntity(1) > 0 
    
    def heuristic(self, start_loc:tuple, end_loc:tuple):
        # we make use of the distance formula:
        # distance = sqrt(abs((x2-x1))^2+abs((y2 - yl))^2) abs so we dont get negatives
        x = abs(start_loc[0] - end_loc[0]) 
        y = abs(start_loc[1] - end_loc[1])
        return (x**2 + y**2)**0.5
