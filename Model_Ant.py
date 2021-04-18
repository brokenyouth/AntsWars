import math
from Util import *
class Ant():

    def __init__(self, _x, _y, _angle, _color, _id):
        self.x = _x
        self.y = _y
        self.angle = _angle
        self.color = _color
        self.id = _id

        self.health = 100
        self.direction = Direction(self.angle)
        self.moveSpeed = 75
        self.rotationspeed = 10

        self.lastDirectionUpdate = 0
        self.lastPheromoneUpdate = 0

        self.maxEnergy = 150
        self.energy = 150
        
        self.depositPheromoneEnergy = 0.5

        self.position = (self.x, self.y)
    
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
    
    def setDirection(self, _dir):
        self.direction = _dir
