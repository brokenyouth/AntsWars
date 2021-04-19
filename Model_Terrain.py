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

        self.listAnthils = []
        self.listObstacles = []
        self.listRessource = []
        self.listAnts = []
        self.listSpiders = []

    def getSpiders(self):
        return self.listSpiders
    
    def getObstacles(self):
        return self.listObstacles
    
    def getRessources(self):
        return self.listRessource

    def getAnthils(self):
        return self.listAnthils

    def addSpider(self, x, y, _spider):
        # -- check bounds
        self.grid[y // TILZSIZE ][x // TILZSIZE] = _spider
        self.listSpiders.append( _spider )

    def addAnthil(self, x, y, _anthil):
        # -- check bounds
        self.grid[y // TILZSIZE ][x // TILZSIZE] = _anthil
        self.listAnthils.append( _anthil )
    
    def addObstacle(self, x, y, _obstacle):
        # -- check bounds
        self.grid[y // TILZSIZE][x // TILZSIZE] = _obstacle
        self.listObstacles.append( _obstacle )
    
    def addRessource(self, x, y, _ressource):
        # -- check bounds
        self.grid[y // TILZSIZE][x // TILZSIZE] = _ressource
        self.listRessource.append( _ressource )
    
    def getAt(self, x, y):
        # -- add bounds check
        return self.grid[y // TILZSIZE][x // TILZSIZE]
    
    def getDimensions(self):
        return self.width, self.height
    
    def reset(self):
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        self.listAnthils = []
        self.listObstacles = []
        self.listRessource = []
        self.listAnts = []
        self.listSpiders = []
        