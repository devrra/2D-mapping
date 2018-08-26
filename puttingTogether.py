import paho.mqtt.client as mqtt

##--------------------------- MAP DEFINATIONS --------------------

import pygame
from pygame.locals import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import random
import time
##import csv

pygame.init()

##GLOBALS -----------------------------
display = (800, 600)
mapDisplay = pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
glClearColor(16/255,17/255,52/255,1.0)  ##to set color of map Base.
pygame.display.set_caption('mAp')
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
ax = 0.0
ay = 0.0
vx = 0.0
vy = 0.0
x_ = 0.0
y_ = 0.0
theta_z = 0.0
#finalSurface = -1

def header(x,y,theta):    #orientation to be included.
    s = 0.02
    glBegin(GL_POLYGON)
    glColor3fv((217,24,55))#color of header
    glVertex2f(x-s,y-s)
    glVertex2f(x+s,y-s)
    glVertex2f(x+s,y+s)
    glVertex2f(x-s,y+s)
    glEnd()

##------------------------ connection -----------------------------

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe("meena")

def on_message(client, userdata, msg):
    ## using GLOBALs
    global display, mapDisplay, ax, ay, vx, vy, x_, y_, theta_z, finalSurface
    
    ## getting Data
    mpu_data = eval(msg.payload)    ## type(msg.payload) = bytes
    print('.')
    #print(mpu_data['Ax'],mpu_data['Ay'],mpu_data['Az'],mpu_data['Gx'],mpu_data['Gy'],mpu_data['Gz'])
    #something = 
    ax = random.gauss(mpu_data['Ax'],0.05)*9.81         ## a is translational accelaration.
    ay = random.gauss(mpu_data['Ay'],0.05)*9.81
    az = random.gauss(mpu_data['Az'],1.2)*9.81
    omega_x = mpu_data['Gx']    ## omega is angular velocity(deg/s)
    omega_y = mpu_data['Gy']
    omega_z = mpu_data['Gz']
    
    ## using Data
    #x_, y_ are coordinates of rooms frame.
    theta_z = theta_z+omega_z*(pi/180)
    vx = vx+ax
    vy = vy+ay
    x_ = x_+vx*cos(theta_z)+vy*sin(theta_z)
    y_ = y_+vy*cos(theta_z)-vx*sin(theta_z)
    j = 0
    #print(x,'-----',y)
    while j<10:
        header(x_/1000,y_/1000,theta_z)
        pygame.display.flip()
        j = j+1
    time.sleep(0.1)
    finalSurface = pygame.display.get_surface()
    pygame.image.save(finalSurface, 'F:/projects/ROBOTICs/2Dmappin/CARTO/outputs/problem2Map.png')
    
    
def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    broker = "broker.mqtt-dashboard.com"
    client.connect(broker,1883,60)
    client.loop_forever()
    #global finalSurface
    #pygame.image.save(finalSurface, 'F:/projects/ROBOTICs/2Dmappin/problem2Map.png')

main()

## batch command to open last modified file in the present directory.(maybe you need to replace %F with %%F)
    ##      for /f "eol=: delims=" %F in ('dir /b /od *.py') do @set "newest=%F"
    ##      idle "%newest%"    
