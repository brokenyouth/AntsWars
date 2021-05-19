import math
import random
from Model_Obstacle import *
from Model_Ressource import *
from Model_Anthil import *


from Util import *

class Terrain():

    def __init__(self, _width, _height):
        self.cellSize = 16
        self.width = _width // self.cellSize
        self.height = _height // self.cellSize

        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        print("terrain size -> {} / {}".format(self.width, self.height))

        self.pheromones = []

    def addEntity(self, x, y, _entity):
        # -- check bounds
        if x < 0 or y < 0 or x > (self.width * TILZSIZE) or y > (self.height * TILZSIZE):
            return False
        self.grid[int(y // TILZSIZE) ][int(x // TILZSIZE)] = _entity

    def addPheromone(self, _phero):
        self.pheromones.append( _phero )
    
    def getPheromones(self):
        return self.pheromones
    
    def getAt(self, x, y):
        # -- add bounds check
        if x < 0 or y < 0 or x > (self.width * TILZSIZE) or y > (self.height * TILZSIZE):
            return False
        return self.grid[y][x]
    
    def getDimensions(self):
        return self.width, self.height
    
    def reset(self):
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        self.pheromones = []

    def remove(self, _x, _y):
        self.grid[_y][_x] = None
        
    def hasWallAt(self, x, y, wx, wy):
        if x < 0 or y < 0 or x > wx or y > wy:
            return False
        return type( self.grid[math.floor(y) // TILZSIZE ][math.floor(x) // TILZSIZE ] ) == Obstacle
    
    def hasRessourceInRange(self, x, y):
        if x < 0 or y < 0 or x > (self.width * TILZSIZE) or y > (self.height * TILZSIZE):
            return False
        xgrid, ygrid = math.floor(x // TILZSIZE), math.floor(y // TILZSIZE)
        found = False
        u, v = 0, 0
        for y in range(-1, 2): # check all cell neighbors.
            for x in range(-1, 2):
                if type( self.grid[ y + ygrid ][ x + xgrid ]  ) == Ressource:
                    found = True
                    u, v = x , y
            if found:
                break
        return found, self.grid[ v + ygrid ][ u + xgrid ]
    
    def hasAnthillAt(self, x, y, wx, wy):
        return type( self.grid[math.floor(y) // TILZSIZE ][math.floor(x) // TILZSIZE ] ) == Anthil

    def hasPheromoneInRange(self, x, y, distance = TILZSIZE):
        found = False
        lastphero = None
        for p in self.pheromones: 
            if vectorLength( (x - p.x), (y - p.y) ) < (distance): # find the nearest one
                lastphero = p
                found = True
                break
        return found, lastphero

    def removePheromone(self, _p):
        self.pheromones.remove(_p)

    def clearPheromones(self):
        self.pheromones = []