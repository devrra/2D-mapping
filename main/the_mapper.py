'''
it gets input from arduino robot(in f,l,r) for drawing,
and then it  traces(copies) the path of real robot in turtle. 
'''

import turtle
import random
import serial
#import time

seri = serial.Serial('COM6', 9600)
#l=[]
p = turtle.Pen()
#p = turtle.Turtle(shape = "square")
p.pensize(5)
p.pencolor('red')

def fuck(a):            #to draw according to the gali.
        if a == 'f':
                p.forward(25)
        if a == 'l':
                p.left(random.randint(0,45))            #this 45 is subject to change. based on real angle turned when one unit command is run.
        if a == 'r':
                p.right(random.randint(0,45))
while True:
        if seri.inWaiting():
                gali = seri.read().decode()
                print(gali)
                fuck(gali)
                

