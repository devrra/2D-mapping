import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

baseMapSize = 2
botSize = 0.02
botStep = 4 ## 0.04

s = baseMapSize
baseMapVertex = [
    [ s, s],
    [-s, s],
    [-s,-s],
    [ s,-s]
    ]

r = botSize
botVertex = [
    [ r, r],
    [-r, r],
    [-r,-r],
    [ r,-r]
    ]

mapEdges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0)
    )

botEdges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0)
    )

faces = ((0, 1, 2, 3))

color = [(1,0,0),(0,1,0),(1,1,0),(1,1,1)]   ## r,g,y,w

botCenterPath = [[0, 0]]

c = 0           ## color shift variable of robot. 


def baseMap():
    glBegin(GL_QUADS)
    for face in faces:
        glColor3fv(color[3])
    glEnd()
    
    glBegin(GL_LINES)
    for edge in mapEdges:
        for vertex in edge:
            glVertex2fv(baseMapVertex[vertex])
    glEnd()

def bot(i):
    glBegin(GL_QUADS)
    for face in faces:
            glColor3fv(color[i])
            glVertex2fv(botVertex[face])
    glEnd()
    
    glBegin(GL_LINES)
    for edge in botEdges:
        for vertex in edge:
            glVertex2fv(botVertex[vertex])
    glEnd()

dirSense = 1        ## 0,1
        
def FB(i):
    #print(dirSense%2)
    for vertex in botVertex:
        vertex[dirSense%2] += i/100
    Center = getBotCenter(botVertex)
    global c
    if Center in botCenterPath:
        c = 2
    else:
        c = 0
        botCenterPath.append(Center)
        print(Center)

def getBotCenter(botVertices):   
    #print(botVertices)      
    x =  (int((botVertices[0][0]+botVertices[1][0]+0.0005)*100))//2
    y =  (int((botVertices[0][1]+botVertices[3][1]+0.0005)*100))//2 
    return [x,y]  

file = open('F:/ROBOTICs/2Dmappin/directions.txt','r')
directions = file.read()
limit = len(directions)


def main():
    #pygame.init()
    display = (900,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    global c
    global dirSense

    for n in range(limit):
        if directions[n]=='F':
            FB(-botStep)
        elif directions[n]=='L':    
            dirSense += 1
        elif directions[n]=='R':    
            dirSense += 1
        elif directions[n]=='B':
            FB(botStep)   
        #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        baseMap()
        bot(2-c)        ## c =0,2
        pygame.display.flip()
        pygame.time.wait(100)
        #c = 0  
        
main()

