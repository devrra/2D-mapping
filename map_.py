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
    glEnd()
    
    glBegin(GL_LINES)
    for edge in botEdges:
        for vertex in edge:
            glVertex2fv(botVertex[vertex])
    glEnd()

def horizontal(i):
    for vertex in botVertex:
        vertex[0] += i/100
    Center = getBotCenter(botVertex)
    #print(Center)
    if Center in botCenterPath:
        global c
        c = 2
    else:    
        botCenterPath.append(Center)
        print(Center)
    
        
def vertical(i):
    for vertex in botVertex:
        vertex[1] += i/100
    Center = getBotCenter(botVertex)
    #print(Center)
    if Center in botCenterPath:
        global c
        c = 2
    else:    
        botCenterPath.append(Center)
        print(Center)

def getBotCenter(botVertices):   
    #print(botVertices)      
    x =  (int((botVertices[0][0]+botVertices[1][0]+0.0005)*100))//2
    y =  (int((botVertices[0][1]+botVertices[3][1]+0.0005)*100))//2 
    return [x,y]  

def main():
    #pygame.init()
    display = (900,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    global c

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    horizontal(-botStep)
                    
                if event.key == pygame.K_RIGHT:
                    horizontal(botStep)

                if event.key == pygame.K_UP:
                    vertical(botStep)

                if event.key == pygame.K_DOWN:
                    vertical(-botStep)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0,0,-0.1)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    glTranslatef(0,0,0.1)

        #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        baseMap()
        bot(2-c)        ## c =0,2
        #print(2-c)
        #print(len(botCenterPath))
        pygame.display.flip()
        pygame.time.wait(100)
        c = 0
        


main()

