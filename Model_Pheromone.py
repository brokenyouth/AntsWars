from enum import Enum
from Util import *

class PheromoneState(Enum):
    Ressource = 1,
    Home = 2,


class Pheromone():

    def __init__(self, _x, _y, _state, _color, _rdx, _rdy):
        self.x = _x
        self.y = _y
        self.state = _state
        self.color = _color
        self.intensity = 100

        self.angleToRessource = getAngleBetween(self.x, self.y, _rdx, _rdy)