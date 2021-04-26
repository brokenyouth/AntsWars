class Ressource():

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.quantity = 1000

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def take(self):
        self.quantity -= 1