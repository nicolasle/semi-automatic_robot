# from math import sqrt
# from math import pi
import math

# Objet représentant un point de l'espace à 2D.
# renvoyé par plusieurs méthodes du module tag.py
class Point:
    def __init__(self, xCoord, yCoord):
        self.x=xCoord
        self.y=yCoord
    # def litteral(self):
    #     output="("+str(self.x)+", "+str(self.y)+")"
    #     return output
    def coord(self):
        return [self.x, self.y]
def deg(rad):
    return rad*180/math.pi

def rad(deg):
    return deg*math.pi/180

# Calcule la distance entre 2 objets 'Point'
def distance(pointA, pointB):
    d=math.sqrt((pointA.x-pointB.x)**2+(pointA.y-pointB.y)**2)
    return d

# Calcule le centre de 4 'Point'
def center(pointA, pointB, pointC, pointD):
    xCoord=1/4*(pointA.x+pointB.x+pointC.x+pointD.x)
    yCoord=1/4*(pointA.y+pointB.y+pointC.y+pointD.y)
    c=Point(xCoord, yCoord)
    return c

# Renvoie l'angle trigonométrique de la droite orientée du 'Point' A au 'Point' B
def direction(pointA, pointB):
    y=pointB.y-pointA.y
    x=pointB.x-pointA.x
    return -deg(math.atan2(y,x))%360

# Renvoie un 'Point' au milieu des 'Point' A et 'Point' B
def middle(pointA, pointB):
    xCoord=(pointA.x+pointB.x)/2
    yCoord=(pointA.y+pointB.y)/2
    return Point(xCoord, yCoord)