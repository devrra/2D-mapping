import pygame
from pygame.locals import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import time
import csv

pygame.init()
sourceFile = open('F:/projects/ROBOTICs/2Dmappin/problem2.csv','r')
data = sourceFile.read()
#m = len(data)

def header(x,y,theta):    #orientation to be included.        
##    r = 0.07    
##    glBegin(GL_TRIANGLES)
##    glColor3fv((0,150,255))
##    glVertex3f(x+3*r*sin(theta), y+3*r*cos(theta), 0)
##    glVertex3f(x-r*sin(theta+pi/4), y-r*cos(theta+pi/4), 0)
##    glVertex3f(x+r*cos(theta+pi/4), y-r*sin(theta+pi/4), 0)
##    glEnd()
    s = 0.02
    glBegin(GL_POLYGON)
    glColor3fv((217,24,55))#color of header
    glVertex2f(x-s,y-s)
    glVertex2f(x+s,y-s)
    glVertex2f(x+s,y+s)
    glVertex2f(x-s,y+s)
    glEnd()

def main():
    display = (800, 600)
    mapDisplay = pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
    glClearColor(16/255,17/255,52/255,1.0)  ##to set color of map Base.
    pygame.display.set_caption('mAp')
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    ax, ay = 0.0, 0.0
    vx, vy = 0.0, 0.0
    x_, y_ = 0.0, 0.0
    theta = 0.0
    with open('F:/projects/ROBOTICs/2Dmappin/problem2.csv','rt') as csvfile:
        #read ax,ay,angular velocity(omega)<deg/s>.
        reader = csv.reader(csvfile,delimiter = ',')
        for row in reader:
            ax, ay, theta = row
            ax = float(ax)
            ay = float(ay)
            theta = float(theta)*(pi/180)
            #x_, y_ are coordinates of rooms frame.
            #theta = theta+omega*(pi/180)
            #ay_ = ay*cos(theta)-ax*sin(theta)
            #ax_ = ay*sin(theta)+ay*cos(theta)
            vx = vx+ax
            vy = vy+ay
            x_ = x_+vx*cos(theta)+vy*sin(theta)
            y_ = y_+vy*cos(theta)-vx*sin(theta)
            j = 0
            #print(x,'-----',y)
            while j<10:
                header(x_/100,y_/100,theta)
                pygame.display.flip()
                j = j+1
            time.sleep(0.1)
            finalSurface = pygame.display.get_surface()
    pygame.image.save(finalSurface, 'F:/projects/ROBOTICs/2Dmappin/problem2Map.png')        
            
    
main()
