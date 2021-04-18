import pygame
import math
from Util import *

class Renderer:

    def __init__(self, _surface,  _terrain, _background):
        self.surface = _surface
        self.terrain = _terrain
        self.background = _background

        self.antImage = pygame.image.load('./data/res/ant_3.png')
        self.antImage = pygame.transform.flip(self.antImage, False, False)
        self.antImage = pygame.transform.smoothscale(self.antImage, (int(107 / TILZSIZE), int(71 / TILZSIZE)))

        self.anthils = self.terrain.getAnthils()
    
    def renderObtsacles(self):
        for obstacle in self.terrain.getObstacles():
            square = pygame.draw.rect( self.surface, obstacle.color, (obstacle.x, obstacle.y, 100, 50) )

    def renderAnt(self, ant):
        x , y = ant.getX(), ant.getY()
        rotated = pygame.transform.rotate(self.antImage, -toDegree( ant.direction.angle ))
        self.surface.blit(rotated, (x ,y ))
    
    def renderAnthil(self, anthil):
        x, y = anthil.getPosition()
        self.antImage = pgfill( self.antImage, anthil.color )
        circ = pygame.draw.circle( self.surface, anthil.color, (x, y), 10, 0 )
        for ant in anthil.getAnts():
            self.renderAnt(ant)
            
    def render(self):
        self.surface.fill(self.background) # effacer l'écran
        # render obstacles
        self.renderObtsacles()
        # render ants
        for anthil in self.terrain.getAnthils():
            self.renderAnthil(anthil)
                