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
        self.antImage = pygame.transform.smoothscale(self.antImage, ( ANT_SIZEX, ANT_SIZEY ))

        self.spiderImage = pygame.image.load('./data/res/spider_3.png')
        self.spiderImage = pygame.transform.flip(self.spiderImage, False, False)
        self.spiderImage = pygame.transform.smoothscale(self.spiderImage, ( SPIDER_SIZEX, SPIDER_SIZEY ) )

        self.anthillImage = pygame.image.load('./data/res/anthill.png')
        self.anthillImage = pygame.transform.flip(self.anthillImage, False, False)
        self.anthillImage = pygame.transform.smoothscale(self.anthillImage, ( ANTHILL_SIZEX, ANTHILL_SIZEY ) )

        self.pheromoneImage = pygame.image.load('./data/res/marker.png')
        self.pheromoneImage = pygame.transform.flip(self.pheromoneImage, False, False)
        self.pheromoneImage = pygame.transform.smoothscale(self.pheromoneImage, ( PHEROMONE_SIZEX , PHEROMONE_SIZEY ) )

        self.redAnt = pgfill(self.anthillImage, (255, 0, 0, 255))
        self.blueAnt = pgfill(self.anthillImage, (0, 75, 255, 255))
        self.greenAnt = pgfill(self.anthillImage, (0, 255, 0, 255))
        self.yellowAnt = pgfill(self.anthillImage, (255, 255, 0, 255))

    def renderPheromone(self, pheromone):
        pygame.draw.ellipse ( self.surface, pheromone.color , (pheromone.x, pheromone.y, 3, 3) )

    def renderRessource(self, ressource):
        x , y = ressource.getX(), ressource.getY()
        pygame.draw.ellipse ( self.surface, (144, 144, 144, 255) , (x - TILZSIZE//2, y - TILZSIZE//2, TILZSIZE, TILZSIZE) )
    
    def renderSpider(self, spider):
        x, y = spider.getX(), spider.getY()
        rotated = pygame.transform.rotate(self.spiderImage, -toDegree( spider.direction.angle ))
        self.surface.blit(rotated, (x - 55//2 , y - 25 // 2))

    def renderObtsacle(self, obstacle):
        pygame.draw.rect( self.surface, obstacle.color, (obstacle.x - TILZSIZE//2 , obstacle.y - TILZSIZE//2 , TILZSIZE, TILZSIZE) )

    def renderAnt(self, ant):
        x , y = ant.getX(), ant.getY()
        dirX, dirY = ant.direction.getVec()
        rotated = pygame.transform.rotate(self.antImage, -toDegree( ant.direction.angle ))
        self.surface.blit(rotated, (x ,y ))
        if ant.getIsCarryingRessource():
            pygame.draw.ellipse ( self.surface, (144, 144, 144, 255) , (x + 2 * dirX , y + 2 * dirY, 4 , 4) )
    
    def renderAnthil(self, anthil):
        x, y = anthil.getPosition()
        # draw anthill
        self.anthillImage = pgfill( self.anthillImage, anthil.color )
        self.surface.blit(self.anthillImage, (x - 12 , y - 12) )
        # draw ants
        self.antImage = pgfill( self.antImage, anthil.color )
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
        for p in self.terrain.getPheromones():
            self.renderPheromone(p)

            
    def render(self):
        self.surface.fill(self.background) # effacer l'écran
        # render world entities
        self.renderWorld()
        
                