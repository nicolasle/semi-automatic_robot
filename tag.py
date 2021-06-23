from coord import Point
import coord
import numpy as np

# Objet tag. Contient plusieurs infos comme les coins, le centre, l'id, ...
class Tag:
    def __init__(self, corner, identifier):  #corners est un tableau de 4 tableaux, id est un nombre
        self.corners=corner
        self.upperLeft=Point(corner[0][0],corner[0][1])
        self.upperRight=Point(corner[1][0],corner[1][1])
        self.lowerRight=Point(corner[2][0],corner[2][1])
        self.lowerLeft=Point(corner[3][0],corner[3][1])
        self.center=coord.center(self.lowerRight, self.lowerLeft, self.upperLeft, self.upperRight)
        self.id=identifier
        self.middleUp = Point(coord.middle(self.upperLeft, self.upperRight).x, coord.middle(self.upperLeft, self.upperRight).y)
        self.middleDown = Point(coord.middle(self.lowerLeft, self.lowerRight).x, coord.middle(self.lowerLeft, self.lowerRight).y)
        self.notFound=0

# Groupe de tags. Contient des méthodes facilitant la recherche d'un certain id, la récupération d'un objet 'Tag' s'il est présent.
# La collection est construite sur base d'un tableau de 'Tag'
class TagCollection:
    def __init__(self, tags):
        # self.tagNotFound=[]
        self.tagArray=tags
        self.size=len(tags)
    def id(self, i):
        for t in self.tagArray:
            if t.id==i:
                return t
        return -1

    def isTagPresent(self, identifier):
        for t in self.tagArray:
            if t.id==identifier:
                return True
        # self.tagNotFound[identifier]=self.tagNotFound[identifier]+1
        return False

# Prend en entrée le résultat du scan, et renvoie une 'TagCollection".
def extractTags(corners, ids):
    tags=[]
    i=0
    for corner in corners:
        tag=Tag(corner[0], ids[i][0])
        i+=1
        tags.append(tag)
    result= TagCollection(tags)
    return result

# Trie les tags d'une 'TagCollection' par ordre croissant d'id
def sortTags(tags):
    sortedTags=[]
    ids=[]
    for t in tags:
        ids.append(t.id)
    ids=np.sort(ids)
    for i in ids:
        for t in tags:
            if t.id==i:
                sortedTags.append(t)
    result=TagCollection(sortedTags)
    return result

# Combine les méthodes d'extraction et de tri
def extractAndSortTags(corners, ids):
    tags=extractTags(corners, ids)
    tags=sortTags(tags.tagArray)
    return tags
