class GameAgent:
    def __init__(self,value,  row, col):
        self._value = value
        self._state = True # the entity is active
        self._startLoc = (row, col)
        self._currentLoc = (row, col)
        self._path = [self._startLoc]
        self._turn = 0
        self._type = ''
    
    def __repr__(self) -> str:
        return str(self._currentLoc)
    
    def updateLoc(self, r, c):
        self._currentLoc = (r, c)
        self._path.append((r,c))

    def updateTurn(self):
        self._turn += 1 

    def dead(self):
        self._state = False
        
    