import cv2
import cv2.aruco as aruco
import tag as tagManager
import pygame
import numpy as np

# Définition du dictionnaire, des paramètres AruCo et de la caméra
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
arucoParameters = aruco.DetectorParameters_create()
cap = cv2.VideoCapture(0)

def make_1080p():
    cap.set(3, 1920)
    cap.set(4, 1080)
def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)
def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)
def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

# make_480p()


# Capture une image et cherche des tags dedans.
# Recommence tant que ce n'est pas réussi
def scanAllTags():
    succeeded=False
    while not succeeded:
        pygame.event.get()
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParameters)
        tags = tagManager.extractAndSortTags(corners, ids)
        cv2.imshow('frame', frame)
        if tags.size>0:
            succeeded=True
    return tags

# Recherche les tags 10, 11, 12, 13.
# Aplatit l'image afin que les 4 tags forment un carré
# Il semblerait que la détection de tags dans l'image aplatie ne fonctionne pas
def doCalibration(img_size):
    tags=scanAllTags()
    if not tags.isTagPresent(10) or not tags.isTagPresent(11) or not tags.isTagPresent(12) or not tags.isTagPresent(13):
        return False, None
    src = np.array([tags.id(12).center.coord(),tags.id(13).center.coord(),tags.id(11).center.coord(),tags.id(10).center.coord()], dtype='float32')
    dst = np.array([[(img_size[0]-100)/2, (img_size[1]-100)/2], [(img_size[0]+100)/2, (img_size[1]-100)/2], [(img_size[0]+100)/2, (img_size[1]+100)/2], [(img_size[0]-100)/2, (img_size[1]+100)/2]], dtype='float32')
    M = cv2.getPerspectiveTransform(src, dst)
    return True, M