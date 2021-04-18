import math
import random

TILZSIZE = 16
PI = 3.1415

WIN_WIDTH = 1600
WIN_HEIGHT = 900

MOVESPEED = 100
ROTATIONSPEED = 1
DIRECTIONRANGE = PI * 0.30
DIRECTIONUPDATERATE = 0.125

def dot(x1, y1, x2, y2):
	return x1 * x2 + y1 * y2

def getRandDirectionRange():
    return random.uniform(-DIRECTIONRANGE, DIRECTIONRANGE)

def getRandRange(val):
    return random.uniform(-val, val)

def getRandUnder(val):
    return random.uniform(0, val)

def toDegree(a):
    return (180 * a) / PI

class Direction:
    def __init__(self, _angle, _rotationspeed = 20):
        self.angle = _angle
        self.targetangle = _angle
        self.rotationspeed =  _rotationspeed
        self.x = 0
        self.y = 0

        self.updateVec()
        self.targetX, self.targetY = self.x, self.y
    
    def updateVec(self):
        self.x = math.cos(self.angle)
        self.y = math.sin(self.angle)
    
    def updateTarget(self):
        self.targetX = math.cos(self.targetangle)
        self.targetY = math.sin(self.targetangle)

    def update(self, dt):
        self.updateVec()

        dir_dt = dot(self.targetX, self.targetY, -self.y, self.x )
        self.angle += ( (ROTATIONSPEED * dir_dt * dt) )


    def getVec(self):
        return (self.x, self.y)

    def setTarget(self, _a):
        self.targetangle = _a
        self.updateTarget()
    
    def addTarget(self, _a):
        self.targetangle += _a
        self.updateTarget()

    def getAngle(self):
        return self.angle % (2*PI)
    