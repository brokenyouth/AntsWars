# DO NOT TOUCH THIS!
# -----------------
import math
import random
import pygame as pg
from enum import Enum

# DO NOT TOUCH THIS!
# -----------------
global MOVESPEED
global PHEROMONEDISPRATE
global CURRENTMODE
global EDITMODE
global DRAGFLAG

# DO NOT TOUCH THIS!
# -----------------

TILZSIZE = 18
PI = 3.1415

WIN_WIDTH = 1024
WIN_HEIGHT = 768

DEFAULTMOVESPEED = 100
MOVESPEED = 100
ROTATIONSPEED = 5
DIRECTIONRANGE = PI * 0.05
DIRECTIONUPDATERATE = 0.125

HOMEUPDATERATE = 5

PHEROMONEDEPOSITRATE = 0.25
PHEROMONEDISPRATE = 0.1

DEFAULT_ANTHIL_POSITIONS = [ (145, 145), (845, 145), (145, 680), (845, 680) ]
DEFAULT_ANTHIL_COLOR = [ (255, 0, 0, 255) , (0, 255, 0, 255), (0, 75, 255, 255), (255, 255, 0, 255) ]

DRAGFLAG = False

ANT_SIZEX, ANT_SIZEY = (107 // (TILZSIZE//2)), (71 // (TILZSIZE//2))
ANTHILL_SIZEX, ANTHILL_SIZEY = 25, 25 
SPIDER_SIZEX, SPIDER_SIZEY = 55, 25
PHEROMONE_SIZEX, PHEROMONE_SIZEY = 11, 7


# DO NOT TOUCH THIS!
# -----------------

def flip_biased_coin(p=0.05):
        return 1 if random.random() < p else 0

class EditMode(Enum):
    RESSOURCE_MODE = 1
    OBSTACLE_MODE = 2
    ANTHILL_MODE = 3
    SPIDER_MODE = 4
    ENABLE = 5
    DISABLE = 6


def pgfill(surface, color):
    """
    Fill all pixels of the surface with color, preserve transparency.
    Avoid using this in a loop.
    """
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

def vectorLength(x, y):
    return math.sqrt( (x * x) + (y * y) )

def getAngleBetween( x1, y1, x2, y2 ):
    """
    Angle between two points.
    """
    return math.atan2( y2 - y1, x2 - x1 )

def sameCell( x1, y1, x2, y2 ):
    return ( math.floor(x1) == math.floor(x2) ) and ( math.floor(y1) == math.floor(y2) )

class Direction:
    def __init__(self, _angle, _rotationspeed = 20):
        """
        Direction class for every moving entity.
        It will calculate their next direction based on the received 'new' angle.
        """
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
        # updates the angle
        self.updateVec()
        dir_dt = dot(self.targetX, self.targetY, -self.y, self.x ) # dot product between the current angle and target angle
        self.angle += ( (ROTATIONSPEED * dir_dt * dt) )

    def getVec(self):
        return (self.x, self.y)

    def setTarget(self, _a):
        # sets angle value
        self.targetangle = _a
        self.updateTarget()
    
    def addTarget(self, _a):
        # add angle value
        self.targetangle += _a
        self.updateTarget()
    
    def instantRedirect(self, _a):
        # instantly redirects to a new direction
        self.targetangle = _a
        self.updateTarget()
        self.updateVec()

    def getAngle(self):
        return self.angle % (2*PI)
