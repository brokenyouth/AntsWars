import math
import random
from Util import *

class Terrain():

    def __init__(self, _width, _height):
        self.cellSize = 16
        self.width = _width // self.cellSize
        self.height = _height // self.cellSize

        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        print('grid len -> ', len(self.grid), len(self.grid[0]), 'total size ->', len(self.grid) * len(self.grid[0]) )

    def addEntity(self, x, y, _entity):
        # -- check bounds
        self.grid[int(y // TILZSIZE) ][int(x // TILZSIZE)] = _entity
    
    def getAt(self, x, y):
        # -- add bounds check
        return self.grid[y][x]
    
    def getDimensions(self):
        return self.width, self.height
    
    def reset(self):
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        