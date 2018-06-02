'''
this program will generate FLR code of the solution path.
it takes input from ('directions.txt') 
and writes a file ('solutionPath.txt') 
'''
import numpy as np


inputFile = open('directions.txt','r')
directions = inputFile.read()
limit = len(directions)

class botStatus:
    '''
    status = information of position and direction(the bot is facing)

    '''
    def __init__(self, pos, head):  
        '''
        pos and head are a duplet(tuple)
        '''
        self.pos = pos
        self.head = head
    
    def altPos(self):       ## called when 'F' is read.
        newStatus = botStatus(self.pos, self.head)
        newStatus.pos[0] += self.head[0]
        newStatus.pos[1] += self.head[1]
        pathCovered.append(newStatus)

    def altHead(self, side):        ## side = 'R', 'L'
        newStatus = botStatus(self.pos, self.head)
        if self.head[0] != 0:
            if side == 'L':
                newStatus.head = self.head[::-1]
            elif side == 'R':
                newStatus.head = [-i for i in self.head[::-1]]
        elif self.head[0] == 0:
            if side == 'R':
                newStatus.head = self.head[::-1]
            elif side == 'L':
                newStatus.head = [-i for i in self.head[::-1]]    
        pathCovered.append(newStatus)            

    def show(self):
        print([self.pos, self.head])

origin = botStatus([0,0],[0,1])
pathCovered = [origin]      

def getPathStatus():
    for n in range(limit):
        if directions[n]=='F':
            pathCovered[-1].altPos()
        else:
            pathCovered[-1].altHead(directions[n]) 
        pathCovered[-1].show()     

def removeLoops():
    length = len(pathCovered)
    print(length)
    for n in range(length):
        for m in range(length-1, n, -1):
            if pathCovered[m].pos == pathCovered[n].pos:
                del pathCovered[n+1:m]
                length = len(pathCovered)
                print(length)
            print(0)    

def decideSide(init, final):
    if init[0] :
        if (init[0]+final[1]):
            return 'L'
        else:
            return 'R'
    else:
        if (init[1]+final[0]):
            return 'R'
        else:
            return 'L'

def solvePath():
    solutionFile = open('SolutionPath.txt','a')
    length = len(pathCovered)
    for i in range(length-1):
        if pathCovered[i].pos != pathCovered[i+1].pos :
            solutionFile.write('    F')
        elif pathCovered[i].head != pathCovered[i+1].head :   
            side = decideSide(pathCovered[i].head, pathCovered[i+1].head) 
            solutionFile.write('    ' + side)
    solutionFile.close()
    print('Sol file closed')

if __name__ == '__main__':
    getPathStatus()
    removeLoops()
    solvePath()


