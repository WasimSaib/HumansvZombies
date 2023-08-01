from GameAgent import GameAgent
class Zombie(GameAgent):
    def __init__(self, row, col):
        super().__init__(2, row, col)
        self._type = 'Z'
    def __repr__(self) -> str:
        return super().__repr__()
    
    