import math
from enum import Enum
from Util import *

class AntState(Enum):
    EXPLORE = 1,
    TOHOME = 2,
    TORESSOURCE = 3

class Ant():

    def __init__(self, _x, _y, _angle, _color, _id, _state):
        self.x = _x
        self.y = _y
        self.angle = _angle
        self.color = _color
        self.id = _id
        self.state = _state

        self.detectionRadius = 10
        
        self.isCarryingRessource = False

        self.health = 100
        self.direction = Direction(self.angle)
        self.moveSpeed = 75
        self.rotationspeed = 10

        self.lastDirectionUpdate = 0
        self.lastPheromoneUpdate = 0

        self.maxEnergy = 1000
        self.energy = 1000
        
        self.depositPheromoneEnergy = 1

        self.homePosition = (self.x, self.y)

        self.lastKnownRessource = None

    def getId(self):
        return self.id
    
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getAngle(self):
        return self.direction.getAngle()
    def getMoveSpeed(self):
        return self.moveSpeed
    def getDirection(self):
        return self.direction
    def getRotationSpeed(self):
        return self.rotationspeed
    def setPosition(self, x, y):
        self.x = x
        self.y = y
    def addPosition(self, x, y):
        self.x += x
        self.y += y    
    def setAngle(self, _a):
        self.angle = _a
    
    def setEnergy(self, _e):
        self.energy = _e
    
    def getEnergy(self):
        return self.energy
        
    def setDirection(self, _dir):
        self.direction = _dir

    def setCarryingRessource(self, status):
        self.isCarryingRessource = status
    
    def getIsCarryingRessource(self):
        return self.isCarryingRessource

    def dropEnergy(self, _amnt):
        self.energy -= _amnt

    def setState(self,_state):
        self.state = _state
    
    def getState(self):
        return self.state