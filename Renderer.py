import pygame
import math
from Util import *

class Renderer:

    def __init__(self, _surface,  _terrain):
        self.surface = _surface
        self.terrain = _terrain

        self.antImage = pygame.image.load('./data/res/ant_3.png')
        self.antImage = pygame.transform.flip(self.antImage, False, False)
        self.antImage = pygame.transform.smoothscale(self.antImage, (11, 7))

        self.ants = self.terrain.getAnts() 

    def render(self):
        BLACK = (0, 0, 0)
        WHITE = (200, 200, 200)
        self.surface.fill(BLACK) # effacer l'écran
        # render grid
        mapX, mapY = self.terrain.getDimensions()
        """for y in range(0,mapY,10):
            for x in range(0,mapX,10):
                u, v = x*(16+1) , y*(16+1)
                self.surface.blit(self.antImage, (u,v))"""

        # render ants
        for ant in self.ants:
            x , y = ant.getX(), ant.getY()
            rotated = pygame.transform.rotate(self.antImage, -toDegree( ant.direction.angle ))
            self.surface.blit(rotated, (x,y))
                