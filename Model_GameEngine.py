import pygame
from Model_Ant import *
from Model_Obstacle import *
from Renderer import *
from Util import *
class GameEngine():

    def __init__(self, _world, _mngr, _surface):
        self.world = _world
        self.manager = _mngr
        self.surface = _surface
        self.worldSizeX, self.worldSizeY = self.world.getDimensions()
        self.renderer = None

        self.surfaceWidth = self.surface.get_width()
        self.surfaceHeight = self.surface.get_height()

    def start(self):
        self.renderer = Renderer(self.surface, self.world)

        ant_id = 0
        for k in range(0, 100):
            x, y = (self.worldSizeX//2), (self.worldSizeY//2)
            ant = Ant(x*TILZSIZE, y*TILZSIZE, getRandRange(2 * PI), ant_id)
            ant.lastDirectionUpdate = getRandUnder(100) * 0.01 * DIRECTIONUPDATERATE
            self.world.addAnt(x, y, ant)
            ant_id += 1

    def handleEvent(self, _event):
        if _event.type == pygame.K_SPACE:
            pass
    
    def updateAnts(self, dt):
        for ant in self.world.getAnts():
            ant_direction = ant.getDirection()
            dirX, dirY = ant_direction.getVec()
            x = (MOVESPEED * dt) * dirX
            y = (MOVESPEED * dt) * dirY

            if ant.x < 0:
                x = self.surfaceWidth
            elif ant.y < 0:
                y = self.surfaceHeight
            elif ant.x > self.surfaceWidth:
                ant.x = 0
            elif ant.y > self.surfaceHeight:
                ant.y = 0
            
            ant.lastDirectionUpdate += dt
            if ant.lastDirectionUpdate > DIRECTIONUPDATERATE:
                randDir = getRandDirectionRange()
                ant.direction.addTarget(randDir)
                ant.lastDirectionUpdate = 0

            ant.addPosition(x,y)
            ant.direction.update(dt)
            #print('ant dir -> ', ant.getDirection().getVec())
            #print('ant angle -> ', ant.getAngle())

            #print('Ant position : {} / {}'.format(ant.x, ant.y))

    def update(self, dt):
        self.manager.update(dt)
        self.updateAnts(dt)

    def render(self):
        self.renderer.render()