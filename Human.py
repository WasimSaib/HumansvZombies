from GameAgent import GameAgent
class Human(GameAgent):
    def __init__(self, row, col):
        super().__init__(1, row, col)
        self._type =  'H'        
    