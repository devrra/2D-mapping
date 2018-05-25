'''
opens an instruction file.
moves bot(yellow square) accordingly on pygame window
saves the last frame of the window as JPEG.
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

faces = ((0, 1, 2, 3))              ## face of yellow square representing bot.

color = [(1,0,0),(0,1,0),(1,1,0),(1,1,1)]   ## r,g,y,w

botCenterPath = [[0, 0]]

c = 0           ## responsible for changing bot to red on retraced path. 
pointer = 0     ## index pointer to the list :direction=[0,2,1,3]


def baseMap():
    '''
    to draw a white square representing map area. 
    '''
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
    '''
    to draw a yellow square representing map area. 
    '''
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

        
def FB(dir):         
    '''
    to move the bot in proper direction.
        this properly maps from <dir>('R','F','L')------->{n,e,s,w}
        and sets the vertex of the bot(yellow square)
    '''
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
        #print(Center)

def getBotCenter(botVertices):         
    x =  (int((botVertices[0][0]+botVertices[1][0]+0.0005)*100))//2
    y =  (int((botVertices[0][1]+botVertices[3][1]+0.0005)*100))//2 
    return [x,y]  

file = open('F:/projects/ROBOTICs/2Dmappin/directions.txt','r')         ## instruction file.
directions = file.read()
limit = len(directions)


def main():
    display = (900,800)
    pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    direction = [0,2,1,3]       ## {n,e,s,w}
    global c                    ## responsible for changing bot to red on retraced path.
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

