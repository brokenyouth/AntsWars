import pygame
from Model_Ant import *
from Model_Obstacle import *
from Model_Anthil import *
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
    
    def initGame(self, nbAnthils, nbAntPerAnthil ):
        for n in range(nbAnthils):
            x, y = DEFAULT_ANTHIL_POSITIONS[ n % len(DEFAULT_ANTHIL_POSITIONS) ]
            color = DEFAULT_ANTHIL_COLOR[ n % len(DEFAULT_ANTHIL_POSITIONS) ]
            anthil = Anthil(x , y  , nbAntPerAnthil, color)
            for i in range(nbAntPerAnthil):
                ant = Ant(x, y, getRandRange(2 * PI), color, i)
                ant.lastDirectionUpdate = getRandUnder(100) * 0.01 * DIRECTIONUPDATERATE
                ant.color = color # mettre un setColor ici plus tard
                anthil.addAnt( ant )
            self.world.addAnthil( x, y, anthil )
        
        obstacle = Obstacle(self.surfaceWidth//2, self.surfaceHeight//2, (255, 255, 255, 255))
        print(obstacle)
        #self.world.addObstacle(obstacle.getX(), obstacle.getY(), obstacle.getColor())

    def start(self):
        bg = self.manager.get_theme().get_colour('dark_bg')
        self.renderer = Renderer(self.surface, self.world, bg)
        self.initGame( 4, 100 ) # 4 by 20

    def handleEvent(self, _event):
        if _event.type == pygame.K_SPACE:
            pass
    
    def updateAnts(self, anthil, dt):
        for ant in anthil.getAnts():
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

    def update(self, dt):
        self.manager.update(dt)
        for anthil in self.world.getAnthils():
            self.updateAnts(anthil, dt)

    def render(self):
        self.renderer.render()