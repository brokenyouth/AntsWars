import math
from Util import *
class Spider():

    def __init__(self, _x, _y, _angle, _id):
        self.x = _x
        self.y = _y
        self.angle = _angle
        self.id = _id

        self.health = 100
        self.direction = Direction(self.angle)
        self.moveSpeed = 75

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
