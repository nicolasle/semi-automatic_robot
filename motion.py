import serial
import time
import coord
import math
import pygame
import scanTags

ser = serial.Serial('COM4', 9600)  # COM4 pour le bluetooth habituellement

batteryCoefficientLine=0.0005*1.1
batteryCoefficientRot=0.005*1.1
sleepDuration=0.7

# Fonctions utiles au mouvement du robot
def forward():
    ser.write(bytes('z', 'utf-8'))


def backward():
    ser.write(bytes('s', 'utf-8'))


def left():
    ser.write(bytes('q', 'utf-8'))


def right():
    ser.write(bytes('d', 'utf-8'))


def stop():
    ser.write(bytes('a', 'utf-8'))


def rLeft():
    ser.write(bytes('L', 'utf-8'))


def rRight():
    ser.write(bytes('R', 'utf-8'))

def computeMisalignement(robotTag, destinationTag):
    robotDirection = coord.direction(robotTag.middleDown, robotTag.middleUp)
    destinationDirection = coord.direction(robotTag.center, destinationTag.center)
    misalignement = (robotDirection - destinationDirection) % 360
    if misalignement < 180:
        return misalignement
    else:
        return misalignement - 360

def computeMisalignementPoint(robotTag, destinationPoint):
    robotDirection = coord.direction(robotTag.middleDown, robotTag.middleUp)
    destinationDirection = coord.direction(robotTag.center, destinationPoint)
    misalignement = (robotDirection - destinationDirection) % 360
    if misalignement < 180:
        return misalignement
    else:
        return misalignement - 360



# Objectif : aligner le robot dans la direction du 'Tag' destinationTag.
# L'alignement est défini à une certaine angleTol près
def align(robotTag, destinationTag, win):
    angleTol = 5                                                                                                        #Tolérance sur l'alignement
    misalignement = computeMisalignement(robotTag, destinationTag)                                                     #Écart d'alignement entre le robot et le destinationTag
    destinationId = destinationTag.id
    robotId = robotTag.id                                                                                               #Récupération des id des 2 tags
    while math.fabs(misalignement) > angleTol:
        pygame.event.get()
        win.fill((0, 0, 255))
        foundTags = scanTags.scanAllTags()                                                                              #On commence par la recherche de tags dans l'image
            #-----------------------#
            #|      Graphics       |#
            #-----------------------#
        if foundTags.isTagPresent(destinationId):
            destinationTag = foundTags.id(destinationId)                                                                #Actualisation de la destination
            pygame.draw.circle(win, (0, 255, 0), [destinationTag.center.x, destinationTag.center.y], 1)                 #Dessin d'un point à la destination
        if foundTags.isTagPresent(robotId):
            robotTag = foundTags.id(robotId)
            xRobot = robotTag.center.x
            yRobot = robotTag.center.y
            pygame.draw.polygon(win, (255, 0, 0), robotTag.corners)
            pygame.draw.line(win, (255, 0, 255), robotTag.center.coord(),
                             coord.middle(robotTag.upperLeft, robotTag.upperRight).coord(), width=2)
            pygame.draw.circle(win, (0, 255, 0), [xRobot, yRobot], 1)
        pygame.draw.line(win, (0, 0, 0), destinationTag.center.coord(), robotTag.center.coord(), width=2)
        pygame.display.flip()

        misalignement = computeMisalignement(robotTag, destinationTag)

        if math.fabs(misalignement)<angleTol:                                                                           #Si on est assez aligné, on sort
            break
        if misalignement > 0:                                                                                           #destinationDirection < robotDirection -> il faut tourner vers la gauche
            right()
            # print("sent left")
        else:
            left()
            # print("sent right")
        time.sleep(batteryCoefficientRot*math.fabs(misalignement))
        stop()
        time.sleep(sleepDuration)
    stop()
    return misalignement

# S'aligne en direction d'un point
def alignPoint(robotTag, destinationPoint, win):
    angleTol = 5                                                                                                        #Tolérance sur l'alignement
    misalignement = computeMisalignementPoint(robotTag, destinationPoint)                                                     #Écart d'alignement entre le robot et le destinationTag
    robotId = robotTag.id                                                                                               #Récupération des id des 2 tags
    while math.fabs(misalignement) > angleTol:
        pygame.event.get()
        win.fill((0, 0, 255))
        foundTags = scanTags.scanAllTags()                                                                              #On commence par la recherche de tags dans l'image
            #-----------------------#
            #|      Graphics       |#
            #-----------------------#
        pygame.draw.circle(win, (0, 255, 0), destinationPoint.coord(), 1)                                               #Dessin d'un point à la destination
        if foundTags.isTagPresent(robotId):
            robotTag = foundTags.id(robotId)
            xRobot = robotTag.center.x
            yRobot = robotTag.center.y
            pygame.draw.polygon(win, (255, 0, 0), robotTag.corners)
            pygame.draw.line(win, (255, 0, 255), robotTag.center.coord(),
                             coord.middle(robotTag.upperLeft, robotTag.upperRight).coord(), width=2)
            pygame.draw.circle(win, (0, 255, 0), [xRobot, yRobot], 1)
        pygame.draw.line(win, (0, 0, 0), destinationPoint.coord(), robotTag.center.coord(), width=2)
        pygame.display.flip()

        misalignement = computeMisalignementPoint(robotTag, destinationPoint)

        if math.fabs(misalignement)<angleTol:                                                                           #Si on est assez aligné, on sort
            break
        if misalignement > 0:                                                                                           #destinationDirection < robotDirection -> il faut tourner vers la gauche
            right()
            # print("sent left")
        else:
            left()
            # print("sent right")
        time.sleep(batteryCoefficientRot*math.fabs(misalignement))
        stop()
        time.sleep(sleepDuration)
        # print(str(misalignement))
    stop()
    return misalignement

def measureDistance():
    ser.write(bytes('m', 'utf-8'))
    received=ser.readline()
    distance=float(received)
    return distance

def getScale(robotTag):
    midUp=coord.middle(robotTag.upperLeft, robotTag.upperRight)
    midDown=coord.middle(robotTag.lowerLeft, robotTag.lowerRight)
    dist=coord.distance(midUp, midDown)
    return dist/6

# Objectif : arriver en ligne droite sur la destination
# Marche à suivre :
# - Tant que le centre du robot est éloigné de la destination de plus de distanceArrived, on boucle :
#       - Tant qu'on est aligné à moins de alignementTol près, on avance pdt sleepDurations et on check l'alignement. Si la distance robot-destinationTag est inférieure à distance Arrived, on break
def goStraightDestination(robotTag, destinationTag, win):
    destinationId = destinationTag.id
    robotId = robotTag.id  # Récupération des id des 2 tags
    distanceArrived=25
    alignementTol=15
    distanceToDestination=coord.distance(robotTag.center, destinationTag.center)
    while distanceToDestination>distanceArrived:
        misalignement=align(robotTag, destinationTag, win)
        while math.fabs(misalignement)<alignementTol:
            # print(robotTag.notFound)
            pygame.event.get()
            if(measureDistance()<=41):
                right()
                time.sleep(batteryCoefficientRot*100)
                stop()
                time.sleep(0.03)
                forward()
                time.sleep(0.5)
                stop()
            forward()
            time.sleep(batteryCoefficientLine*distanceToDestination)
            stop()
            time.sleep(sleepDuration)
            foundTags = scanTags.scanAllTags()
            pygame.event.get()
            win.fill((0, 0, 255))
            if foundTags.isTagPresent(destinationId):
                destinationTag = foundTags.id(destinationId)                                                                #Actualisation de la destination
                pygame.draw.circle(win, (0, 255, 0), [destinationTag.center.x, destinationTag.center.y], 1)
            if foundTags.isTagPresent(robotId):
                robotTag = foundTags.id(robotId)
                xRobot = robotTag.center.x
                yRobot = robotTag.center.y
                pygame.draw.polygon(win, (255, 0, 0), robotTag.corners)
                pygame.draw.line(win, (255, 0, 255), robotTag.center.coord(),
                             coord.middle(robotTag.upperLeft, robotTag.upperRight).coord(), width=2)
                pygame.draw.circle(win, (0, 255, 0), [xRobot, yRobot], 1)
            else:
                robotTag.notFound=robotTag.notFound+1
                if robotTag.notFound>5:
                    foundTags = scanTags.scanAllTags()
                    while not foundTags.isTagPresent(robotId):
                        # print("Where are you dad ?")
                        backward()
                        time.sleep(sleepDuration)
                        stop()
                        time.sleep(2)
                        foundTags = scanTags.scanAllTags()
            pygame.draw.line(win, (0, 0, 0), destinationTag.center.coord(), robotTag.center.coord(), width=2)
            pygame.display.flip()
            misalignement=computeMisalignement(robotTag, destinationTag)
            # print(misalignement)
            distanceToDestination=coord.distance(robotTag.center, destinationTag.center)
            if distanceToDestination<distanceArrived:
                break
    # print("Bien arrivé, bisous à la famille !")
    return True

def goStraightPoint(robotTag, destinationPoint, win):
    robotId = robotTag.id  # Récupération des id des 2 tags
    distanceArrived = 25
    alignementTol = 15
    distanceToDestination = coord.distance(robotTag.center, destinationPoint)
    while distanceToDestination > distanceArrived:
        misalignement = alignPoint(robotTag, destinationPoint, win)
        while math.fabs(misalignement) < alignementTol:
            # print(robotTag.notFound)
            pygame.event.get()
            forward()
            time.sleep(batteryCoefficientLine * distanceToDestination)
            stop()
            time.sleep(sleepDuration)
            foundTags = scanTags.scanAllTags()
            pygame.event.get()
            win.fill((0, 0, 255))
            pygame.draw.circle(win, (0, 255, 0), destinationPoint.coord(), 1)
            if foundTags.isTagPresent(robotId):
                robotTag = foundTags.id(robotId)
                xRobot = robotTag.center.x
                yRobot = robotTag.center.y
                pygame.draw.polygon(win, (255, 0, 0), robotTag.corners)
                pygame.draw.line(win, (255, 0, 255), robotTag.center.coord(),
                                 coord.middle(robotTag.upperLeft, robotTag.upperRight).coord(), width=2)
                pygame.draw.circle(win, (0, 255, 0), [xRobot, yRobot], 1)
            else:
                robotTag.notFound = robotTag.notFound + 1
                if robotTag.notFound > 5:
                    foundTags = scanTags.scanAllTags()
                    while not foundTags.isTagPresent(robotId):
                        # print("Where are you dad ?")
                        backward()
                        time.sleep(sleepDuration)
                        stop()
                        time.sleep(2)
                        foundTags = scanTags.scanAllTags()
            pygame.draw.line(win, (0, 0, 0), destinationPoint.coord(), robotTag.center.coord(), width=2)
            pygame.display.flip()
            misalignement = computeMisalignementPoint(robotTag, destinationPoint)
            # print(misalignement)
            distanceToDestination = coord.distance(robotTag.center, destinationPoint)
            if distanceToDestination < distanceArrived:
                break
    # print("Bien arrivé, bisous à la famille !")
