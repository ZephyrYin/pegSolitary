__author__ = 'zephyryin'

import sys
import time
import copy
import math
import heapq

#@profile
def Astar(config, heu):
    configHistory = []
    expandNodeCnt = 0
    pruneNodeCnt = 0
    solution = []

    root = Node(config, [], 0, heu(config))   # initialize root node

    fringeList = []
    heapq.heapify(fringeList)
    heapq.heappush(fringeList, root)

    while len(fringeList) > 0:
        topNode = heapq.heappop(fringeList)
        expandNodeCnt = expandNodeCnt + 1

        if checkGoal(topNode.config):
            solution = YXpath2posPath(config, topNode.path)
            return expandNodeCnt, pruneNodeCnt, solution

        if checkDuplicate(configHistory, topNode):
            pruneNodeCnt = pruneNodeCnt + 1
            continue

        configHistory[len(topNode.path)].append(copy.deepcopy(topNode.config))            # add status to history list

        pegs = avaPeg(topNode.config)

        for p in pegs:
            curYX = p[0]
            for i in range(1,len(p)):
                sonNode = Node(copy.deepcopy(topNode.config), copy.deepcopy(topNode.path), topNode.gCost, topNode.hCost)
                #sonNode = copy.deepcopy(topNode)
                nextYX = copy.deepcopy(p[i])
                jump(sonNode.config, curYX, nextYX)
                sonNode.path.append([curYX, nextYX])
                sonNode.gCost = sonNode.gCost + 1
                sonNode.hCost = heu(sonNode.config)

                heapq.heappush(fringeList, sonNode)

    return expandNodeCnt, pruneNodeCnt, solution

def manhattanDis(cur,next):
    return abs(cur[0] - next[0]) + abs(cur[1] - next[1])

def heuMan(config):                     # heuristic using manhattan distance
    midYX = [int(len(config)/2), int(len(config[0])/2)]
    sum = 0
    for y in range(len(config)):
        for x in range(len(config[0])):
            if config[y][x] == 'X':
                sum += manhattanDis([y,x],midYX)*0.5
    return sum

def diagonalDis(cur,next):
    return math.hypot(abs(cur[0] - next[0]), abs(cur[1] - next[1]))

def heuDia(config):                     # heuristic using manhattan distance
    midYX = [int(len(config)/2), int(len(config[0])/2)]
    sum = 0
    for y in range(len(config)):
        for x in range(len(config[0])):
            if config[y][x] == 'X':
                sum += diagonalDis([y,x],midYX)*0.5
    return sum

def checkGoal(config):                      # check if the goal state is reached
    midYX = [int(len(config)/2), int(len(config[0])/2)]
    if config[midYX[0]][midYX[1]] != 'X':
        return False
    for y in range(len(config)):
        for x in range(len(config[0])):
            if (y!= midYX[0] or x != midYX[1]) and config[y][x] == 'X':
                return False
    return True

def avaPeg(config):          # find the pegs that could jump, return [ peg, next moves ]
    pegs = []
    for y in range(len(config)):
        for x in range(len(config[y])):
            posList = [[y,x]]
            if config[y][x] == 'X':
                for d in direction:
                    nextY = y + d[0]
                    nextX = x + d[1]
                    if nextY < len(config) and nextY > -1 and nextX < len(config[y]) and nextX > -1 and config[nextY][nextX] == '0':
                        if(config[y+int(d[0]/2)][x+int(d[1]/2)] == 'X'):
                            posList.append([nextY,nextX])
            if len(posList) > 1:
                pegs.append(posList)
    return pegs

class Node(object):
    def __init__(self, config, path, gCost, hCost):
        self.config = config
        self.path = path
        self.gCost = gCost
        self.hCost = hCost

    def printNode(self):
        printCon(self.config)
        print(self.path)
        print('gCost: ', self.gCost)
        print('hCost: ', self.hCost)

    def __lt__(self, other):
        return self.gCost + self.hCost < other.gCost + other.hCost

def genPosTable(config):                    # generate the chessboard based on the configuration
    posTable = []
    cnt = 0
    for cL in config:
        p = []
        for c in cL:
            if c == '-':
                p.append(-1)
            else:
                p.append(cnt)
                cnt = cnt + 1
        posTable.append(p)
    return posTable

def YXpath2posPath(config,YXpath):          # change the yx to pos form
    posTable = genPosTable(config)
    posPath = []
    for ft in YXpath:
        newFt = [posTable[ft[0][0]][ft[0][1]],posTable[ft[1][0]][ft[1][1]]]
        posPath.append(newFt)
    return posPath

def jump(config, curYX, nextYX):                # peg jump from cur to next
    midYX = [int((curYX[0] + nextYX[0])/2),int((curYX[1] + nextYX[1])/2)]
    config[curYX[0]][curYX[1]] = '0'
    config[midYX[0]][midYX[1]] = '0'
    config[nextYX[0]][nextYX[1]] = 'X'

def checkDuplicate(conHistory, node):
    depth = len(node.path)
    if len(conHistory) <= depth:
        conHistory.append([])
        return False

    for c in conHistory[depth]:
        if sameConfig(c, node.config):
            return True
    return False

def antiClock(A):                           # return a matrix anti clock rotated by 90 degrees
    R = [[A[x][y] for x in range(len(A))] for y in range(len(A[0])-1, -1, -1)]
    return R

def sameConfig(A,B):                        # check if two configs are same in 4 rotations
    R = copy.deepcopy(A)
    for d in range(4):
        if d > 0:
            R = antiClock(R)
        if R == B or LeftRightSymetry(R, B) or UpDownSymetry(R, B):
            return True
    return False

def LeftRightSymetry(A, B):
    for y in range(len(A)):
        for x in range(len(A[0])):
            if A[y][x] != B[y][len(A[0])-1-x]:
                return False
    return True


def UpDownSymetry(A, B):
    for y in range(len(A)):
        if A[y] != B[len(A)-1-y]:
            return False
    return True

def str2List(config):
    l = []
    for str in config:
        row = []
        for letter in str:
            row.append(letter)
        l.append(row)
    return l

def printCon(config):
    print('\nconfigurayion:')
    for c in config:
        print(c)


direction = [[-2,0],[0,2],[2,0],[0,-2]]
configutation = ['--000--','--0X0--','00XXX00','000X000','000X000','--000--','--000--']
#configutation = ['--XXX--','--XXX--','XXXXXXX','XXX0XXX','XXXXXXX','--XXX--','--XXX--']
con = str2List(configutation)
printCon(con)
print('')

print('using first heuristic function:')
start = time.clock()
expandNodes1, pruneNodes1, path1 = Astar(con, heuMan)                # use heuristic 1
if len(path1) == 0:
    print('no solution')
else:
    print('solution:')
    print(path1)
elapsed = time.clock() - start
print('expand ', expandNodes1, ' ndoes')
print('prun ', pruneNodes1,' nodes')
print('time used: ',elapsed)

print('')
print('using second heuristic function:')
start = time.clock()
expandNodes2, pruneNodes2, path2 = Astar(con, heuDia)                # use heuristic 2
if len(path2) == 0:
    print('no solution')
else:
    print('soliution:')
    print(path2)
elapsed = time.clock() - start
print('expand ',expandNodes2,' nodes')
print('prun ',pruneNodes2,' nodes')
print('time used: ', elapsed)
