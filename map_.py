'''
--->to be modified to take input from a .txt file
bug in it..
    the (actual)bot will turn to right<R>(say) and then move forward<F>, and accordingly will be the input to the code.
    
    the code (at present) will not continue to draw path in rightward direction once it starts getting <F>s after the <R>.     
'''

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import time

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
pointer = 0


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

        
def FB(dir):          ## i's purpose changed, now not for botStep. 
    #print(dirSense%2)
    i = ((-1)**dir)*botStep
    if dir in [0,1]:
        a = 1
    elif dir in [2,3]:
        a = 0     

    for vertex in botVertex:
        vertex[a] += i/100
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

file = open('F:/projects/ROBOTICs/2Dmappin/directions.txt','r')
directions = file.read()
limit = len(directions)


def main():
    #pygame.init()
    display = (900,800)
    pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    direction = [0,2,1,3]       ## {n,e,s,w}
    global c
    global pointer

    for n in range(limit):
        if directions[n]=='F':
            FB(direction[pointer%4])
        elif directions[n]=='L':    
            pointer -= 1
        elif directions[n]=='R':    
            pointer += 1 
        #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        baseMap()
        bot(2-c)        ## c =0,2
        pygame.display.flip()
        pygame.time.wait(1)
        finalSurface = pygame.display.get_surface()                  
    pygame.image.save(finalSurface, 'F:/projects/ROBOTICs/2Dmappin/test.png')  
        
main()

