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
import os
#import timeit
##import csv

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30,50)
pygame.init()

##GLOBALS -----------------------------
display = (800, 600)
mapDisplay = pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
glClearColor(16/255,17/255,52/255,1.0)  ##to set color of map Base.
pygame.display.set_caption('CARTO')
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
ax = 0.0
ay = 0.0
vx_ = 0.0
vy_ = 0.0
x_ = 0.0
y_ = 0.0
pastTime = 0.0
presentTime = 0.0
oldOmega_z = 0.0
old_ax_ = 0.0
old_ay_ = 0.0
old_vx_ = 0.0
old_vy_ = 0.0
theta_z = 0.0
symbol = '*'

#toDebug
inputPath = 'C:/Users/user/Desktop/omega_z.txt'
outPath = 'C:/Users/user/Desktop/theta_z.txt'

ifile = open(inputPath,'a')
ofile = open(outPath,'a')
ifile.write("===================================================================")
ofile.write("===================================================================")
ifile.close()
ofile.close()

def header(x,y):    #orientation to be included.
    s = 0.02
    glBegin(GL_POLYGON)
    glColor3fv((217,24,55))#color of header
    glVertex2f(x-s,y-s)
    glVertex2f(x+s,y-s)
    glVertex2f(x+s,y+s)
    glVertex2f(x-s,y+s)
    glEnd()
    return

caliberationIndex = 0
delAx = 0.0
delAy = 0.0
delGz = 0.0
def caliberate(ax, ay, gz): 
    global delAx,delAy,delGz
    ## assuming no motion of the bot during caliiberation
    # taking mean
    delAx = delAx + ax
    delAy = delAy + ay
    delGz = delGz + gz
    
    

##------------------------ connection -----------------------------    

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe("meena")

def on_message(client, userdata, msg):
    ## getting GLOBALs
    global display, mapDisplay, ax, ay, vx_, vy_, x_, y_, theta_z, caliberationIndex, symbol 
    global inputPath, outPath, finalSurface, pastTime, presentTime, delAx, delAy, delGz
    global old_ax_, oldOmega_z , old_ay_, old_vy_, old_vx_
    ## getting Data
    try:
        mpu_data = eval(msg.payload)    ## type(msg.payload) = bytes
    except:
        print('||e||')
        return
    
    pastTime = presentTime
    presentTime = time.clock()
    #print(symbol,end = '')
    #print(mpu_data['Ax'],mpu_data['Ay'],mpu_data['Az'],mpu_data['Gx'],mpu_data['Gy'],mpu_data['Gz'])
    ax = mpu_data['Ax']*9.81         ## a is translational accelaration.
    ay = mpu_data['Ay']*9.81
    #az = random.gauss(mpu_data['Az'],1.2)*9.81
    #omega_x = mpu_data['Gx']    ## omega is angular velocity(deg/s)
    #omega_y = mpu_data['Gy']
    omega_z = mpu_data['Gz']*(pi/180)   ## converted in radian/s
    #print(mpu_data['Gz'])
    N = 100
    if caliberationIndex<N:
        caliberate(ax, ay,omega_z)
        caliberationIndex += 1
    elif caliberationIndex==N:
        delAx /= N
        delAy /= N
        delGz /= N
        caliberationIndex += 10
        symbol = '.'
        print('\n\n',delAx, delAy, delGz,'\n\n')  #print('\n\n',delAx,delAy,delGz,'\n\n')
    else:
        ifile = open(inputPath,'a')
        ofile = open(outPath,'a')
        ax = ax - delAx
        ay = ay - delAy
        omega_z = omega_z - delGz
        ## using Data
        #x_, y_ are coordinates of rooms frame.
        theta_z = theta_z+(oldOmega_z+omega_z)*(2/2)*(presentTime-pastTime)
        #theta_z = theta_z + omega_z        ## better output
        ax_ = -ax*sin(theta_z)-ay*cos(theta_z)
        ay_ = ax*cos(theta_z)-ay*sin(theta_z)
        vx_ = vx_+(old_ax_+ax_)*(presentTime-pastTime)/2
        vy_ = vy_+(old_ay_+ay_)*(presentTime-pastTime)/2
        x_ = x_+(old_vx_+vx_)*(presentTime-pastTime)/2
        y_ = y_+(old_vy_+vy_)*(presentTime-pastTime)/2
        j = 0
        oldOmega_z = omega_z
        old_ax_ = ax_
        old_ay_ = ay_
        old_vx_ = vx_
        old_vy_ = vy_
        
        #old_ay = ay
        #print(x,'-----',y)
        while j<10:
            header(x_/1000,y_/1000)
            pygame.display.flip()
            j = j+1
        time.sleep(0.1)     ## 0.1 seconds
        finalSurface = pygame.display.get_surface()
        pygame.image.save(finalSurface, 'F:/projects/ROBOTICs/2Dmappin/CARTO/outputs/problem2Map.png')
        ifile.write(str(omega_z*(180/pi))+'\n')     ## in deg/s
        ofile.write(str(theta_z*(180/pi))+'\n')     ## in deg
        print(theta_z*(180/pi))
        ifile.close()
        ofile.close()
    
def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    broker = "broker.mqtt-dashboard.com"
    client.connect(broker,1883,60)
    global presentTime
    presentTime = time.clock()
    client.loop_forever()
    #global finalSurface
    #pygame.image.save(finalSurface, 'F:/projects/ROBOTICs/2Dmappin/problem2Map.png')

main()

## batch command to open last modified file in the present directory.(maybe you need to replace %F with %%F)
    ##      for /f "eol=: delims=" %F in ('dir /b /od *.py') do @set "newest=%F"
    ##      idle "%newest%"    
