import math
import random
import pygame as pg
from enum import Enum

global MOVESPEED
global PHEROMONEDISPRATE
global CURRENTMODE
global EDITMODE

TILZSIZE = 16
PI = 3.1415

WIN_WIDTH = 1600
WIN_HEIGHT = 900

DEFAULTMOVESPEED = 100
MOVESPEED = 100
ROTATIONSPEED = 5
DIRECTIONRANGE = PI * 0.1
DIRECTIONUPDATERATE = 0.125
PHEROMONEDISPRATE = 0.1

DEFAULT_ANTHIL_POSITIONS = [ (245, 145), (1345, 145), (245, 745), (1345, 745) ]
DEFAULT_ANTHIL_COLOR = [ (255, 0, 0, 255) , (0, 255, 0, 255), (0, 75, 255, 255), (255, 255, 0, 255) ]

class EditMode(Enum):
    RESSOURCE_MODE = 1
    OBSTACLE_MODE = 2
    ANTHILL_MODE = 3
    SPIDER_MODE = 4
    ENABLE = 5
    DISABLE = 6


def pgfill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pg.Color(r, g, b, a))
    return surface

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
        # la direction de la fourmis est le produit scalaire* entre sa normale et sa target
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
    