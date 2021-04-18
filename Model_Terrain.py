import math
import random

class Terrain():

    def __init__(self, _width, _height):
        self.cellSize = 16
        self.width = _width // self.cellSize
        self.height = _height // self.cellSize

        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        print('grid len -> ', len(self.grid), len(self.grid[0]), 'total size ->', len(self.grid) * len(self.grid[0]) )
        self.listObstacles = []
        self.listRessource = []
        self.listAnts = []
    
    def getObstacles(self):
        return self.listObstacles
    
    def getRessources(self):
        return self.listRessource

    def getAnts(self):
        return self.listAnts
    
    def addObstacle(self, x, y, _obstacle):
        # -- check bounds
        self.grid[y][x] = _obstacle
        self.listObstacles.append( (x, y, _obstacle) )
    
    def addRessource(self, x, y, _ressource):
        # -- check bounds
        self.grid[y][x] = _ressource
        self.listRessource.append( (x, y, _ressource) )
    
    def addAnt(self, x, y, _ant):
        # -- check bounds
        self.grid[y][x] = _ant
        self.listAnts.append( _ant )
    
    def getAt(self, x, y):
        # -- add bounds check
        return self.grid[y][x]
    
    def getDimensions(self):
        return self.width, self.height