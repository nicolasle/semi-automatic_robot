import coord
import scanTags
import coord as space
import pygame
import time
import tag
import motion
import math




RED=(255,0,0)
GREEN= (0,255,0)
BLUE=(0,0,255)
PURPLE=(255,0,255)
WHITE=(0,0,0)

robotMarker=0
destinationMarker=2

dim_win=(640,480)
img_size=[640,480]




pygame.init()
win=pygame.display.set_mode(dim_win)
pygame.display.set_caption("AruCo")
win.fill(BLUE)
pygame.display.flip()
destinationTag=tag.Tag([[0,0],[0,0],[0,0], [0,0]], destinationMarker)
robotTag=tag.Tag([[0,0],[0,0],[0,0], [0,0]], destinationMarker)
succeededCalibration = False

points=[[100,100],[540,100],[540,380], [320,240]]
circle=[]
for s in range(10):
    newPoint=[320+150*math.cos(s*2*math.pi/10), 240+150*math.sin(s*2*math.pi/10)]
    circle.append(newPoint)

tagsToExplore=[1,2,3,4,5,6,7]

for currentTagNumber in tagsToExplore:
    destinationReached=False
    destinationMarker=currentTagNumber
    while destinationReached==False:
        win.fill(BLUE)
        destinationTag = tag.Tag([[0, 0], [0, 0], [0, 0], [0, 0]], destinationMarker)
        foundTags = scanTags.scanAllTags()

        if foundTags.isTagPresent(destinationMarker):
            destinationTag=foundTags.id(destinationMarker)
            pygame.draw.circle(win, GREEN, [destinationTag.center.x, destinationTag.center.y], 1)
        if foundTags.isTagPresent(robotMarker):
            robotTag=foundTags.id(robotMarker)
            xRobot = robotTag.center.x
            yRobot = robotTag.center.y
            pygame.draw.polygon(win, RED, robotTag.corners)
            pygame.draw.line(win, PURPLE, robotTag.center.coord(), space.middle(robotTag.upperLeft, robotTag.upperRight).coord(), width=2)
            pygame.draw.circle(win, GREEN, [xRobot, yRobot], 1)
        pygame.draw.line(win, WHITE, destinationTag.center.coord(), robotTag.center.coord(), width=2)
        pygame.display.flip()
        if foundTags.isTagPresent(destinationMarker) and foundTags.isTagPresent(robotMarker):                             #pour aller au tag destinationTag
            destinationReached=motion.goStraightDestination(robotTag, destinationTag, win)
        # if foundTags.isTagPresent(robotMarker):
        #     for i in range(10):
        #         print("Going to "+str(space.Point(circle[i][0], circle[i][1]).coord()))
        #         motion.goStraightPoint(robotTag, space.Point(circle[i][0], circle[i][1]), win)
cap.release()
