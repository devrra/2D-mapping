'''
this program will generate FLR code of the solution path.
it takes input from ('directions.txt') 
and writes a file ('solutionPath.txt') 
'''

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
        newStatus = botStatus(self.pos[:], self.head[:])
        newStatus.pos[0] += self.head[0]
        newStatus.pos[1] += self.head[1]
        pathCovered.append(newStatus)

    def altHead(self, side):        ## side = 'R', 'L'
        newStatus = botStatus(self.pos[:], self.head[:])
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

class Tree:
    def __init__(self, pos, priority):
        self.pos = pos
        self.priority = priority
        self.children = []

    def show(self):
        print(self.pos, self.priority) 

    def insertChild(self, newNode):
        global mother
        if newNode.pos not in [nodeList[i].pos for i in range(len(nodeList))]:
            self.children.append(newNode)
            nodeList.append(newNode)
            mother = newNode
        else:
            mother = [nodeList[i] for i in range(len(nodeList)) if nodeList[i].pos == newNode.pos][0]           

inputFile = open('directions2.txt','r')
directions = inputFile.read()
limit = len(directions)

origin = botStatus([0,0],[0,1])
pathCovered = [origin]    

priority = 1
nodeList = []
mother = None

solutionPos = []
currentHead = [0,1]
solutionDir = []
  
def getPathStatus():
    '''
    this generates the pathCovered list.
    '''
    for n in range(limit):
        if directions[n]=='F':
            pathCovered[-1].altPos()
        elif directions[n] in ['R','L']:
            pathCovered[-1].altHead(directions[n])     

def buildTree():
    global priority
    for n in range(1, len(pathCovered)-1):       ## to create the Tree
        if pathCovered[n].head != pathCovered[n+1].head:
            newNode = Tree(pathCovered[n].pos, priority)
            mother.insertChild(newNode)
            priority += 1

def TravelTree(tree):
    if tree:
        print(tree.pos)
        for child in tree.children:
            TravelTree(child)

def solveTree(tree):
    ## in presentNode, find Child that has highest prority.
    ## append the presentNode.pos in a list, 
    ## make Child the presentNode.
    ## REPEAT.
    presentNode = tree
    if len(presentNode.children) != 0:
        k, m = 0, -1
        for i in range(len(presentNode.children)):
            if presentNode.children[i].priority > m:
                m = presentNode.children[i].priority
                k = i
        Child = presentNode.children[k]
        solutionPos.append(presentNode.pos[:])
        solveTree(Child)
    else:
        solutionPos.append(presentNode.pos[:])
        return None    

def changeHead(reqHead):
    global currentHead
    if reqHead != currentHead:
        a, b = 0, 0
        l = [[1,0],[0,1],[-1,0],[0,-1]]
        for i in range(len(l)):
            if l[i] == currentHead:
                a = i
            if l[i] == reqHead:
                b = i
        n = 10*a+b
        if n in [10, 21, 32, 3]:
            solutionDir.append('R')
        elif n in [30, 1, 12, 23]:
            solutionDir.append('L') 
        elif n in [20, 31, 2, 13]:
            solutionDir.append('R')                    
            solutionDir.append('R')
        currentHead = reqHead    

def generateDirs():
    for i in range(len(solutionPos)-1):
        displacement = [
                        (solutionPos[i+1][0]-solutionPos[i][0]),
                        (solutionPos[i+1][1]-solutionPos[i][1])
                        ]
        reqHead = []
        steps = 0
        for i in displacement:
            if i == 0:
                reqHead.append(i)
            else:
                reqHead.append(i/abs(i))
                steps = abs(i)
        changeHead(reqHead)
        while steps:
            solutionDir.append('F')
            steps -= 1        

if __name__ == '__main__':
    getPathStatus()
    
    start = Tree(pathCovered[0].pos, 0)
    mother = start
    nodeList.append(mother)
    
    buildTree()
    #TravelTree(start)
    solveTree(start)
    generateDirs()

    file = open('SolutionPath.txt', 'w')
    for i in range(len(solutionDir)):
        file.write('    '+solutionDir[i])
