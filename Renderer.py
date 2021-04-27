import pygame
import math
from Model_Ant import *
from Model_Obstacle import *
from Model_Anthil import *
from Model_Spider import *
from Model_Ressource import *
from Util import *

class Renderer:

    def __init__(self, _surface,  _terrain, _background):
        self.surface = _surface
        self.terrain = _terrain
        self.background = _background

        self.antImage = pygame.image.load('./data/res/ant_3.png')
        self.antImage = pygame.transform.flip(self.antImage, False, False)
        self.antImage = pygame.transform.smoothscale(self.antImage, (int(107 / TILZSIZE), int(71 / TILZSIZE)))

        self.spiderImage = pygame.image.load('./data/res/spider_3.png')
        self.spiderImage = pygame.transform.flip(self.spiderImage, False, False)
        self.spiderImage = pygame.transform.smoothscale(self.spiderImage, (int(55), int(25) ) )

    
    def renderRessource(self, ressource):
        x , y = ressource.getX(), ressource.getY()
        pygame.draw.ellipse ( self.surface, (144, 144, 144, 255) , (ressource.x, ressource.y, TILZSIZE*2, TILZSIZE*2) )
    
    def renderSpider(self, spider):
        x, y = spider.getX(), spider.getY()
        rotated = pygame.transform.rotate(self.spiderImage, -toDegree( spider.direction.angle ))
        self.surface.blit(rotated, (x ,y ))

    def renderObtsacle(self, obstacle):
        square = pygame.draw.rect( self.surface, obstacle.color, (obstacle.x, obstacle.y, TILZSIZE, TILZSIZE) )

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

    def renderWorld(self):
        for y in range( int ( WIN_HEIGHT // TILZSIZE)  ):
            for x in range( int ( WIN_WIDTH // TILZSIZE) ):
                
                _object = self.terrain.getAt( x , y )
                if isinstance( _object, Anthil ):
                    self.renderAnthil( _object )
                elif isinstance( _object, Spider ):
                    self.renderSpider( _object )
                elif isinstance( _object, Ressource ):
                    self.renderRessource( _object )
                elif isinstance( _object, Obstacle ):
                    self.renderObtsacle( _object )


            
    def render(self):
        self.surface.fill(self.background) # effacer l'écran
        # render world entities
        self.renderWorld()
        
                