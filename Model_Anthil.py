import pygame

class Anthil:

    def __init__(self, _x, _y, _size, _color, _id):
        self.x = _x
        self.y = _y
        self.size = _size
        self.color = _color
        self.id = _id
        self.score = 0

        self.ants = []

    def getId(self):
        return self.id

    def addAnt(self, _ant):
        self.ants.append(_ant)

    def getPosition(self):
        return self.x, self.y

    def getAnt(self, _id):
        return self.ants[_id]
    
    def getAnts(self):
        return self.ants

    def getScore(self):
        return self.score
    
    def addScore(self):
        self.score += 1