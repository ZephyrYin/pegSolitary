import time
import copy


def DFS(config, conHistory, paths, path, curDep, depth):
    if(curDep > depth):                # exceed the depth limit
        return 0, 0

    if(checkGoal(config)):              # find a path that is right
        posPath = YXpath2posPath(config,path)                    #
        paths.append(posPath)
        return 0, 0

    if checkDuplicate(conHistory, config, curDep):                  # prune current node
        return 0, 1                     # record prune 1 node
    conHistory[curDep].append(copy.deepcopy(config))            # add status to history list

    avaPegs = avaPeg(config)            # find available moves in current status
    nodeCount = 1
    prunNodeCnt = 0
    # for aP in avaPegs:
    #     nodeCount = nodeCount + len(aP) - 1
    for aP in avaPegs:
        cur = aP[0]
        for i in range(1,len(aP)):
            next = aP[i]
            jump(config,cur,next)
            path.append([cur, next])

            #nodeCount = nodeCount + DFS(config, conHistory, paths, path, curDep+1, depth)        # recursive
            cnt = DFS(config, conHistory, paths, path, curDep+1, depth)
            nodeCount = nodeCount + cnt[0]
            prunNodeCnt = prunNodeCnt + cnt[1]
            if len(paths)>0:                    # find one path and exit
                return nodeCount, prunNodeCnt
            backTrack(config,cur,next)
            path.pop()
    return nodeCount, prunNodeCnt
#@profile
def IDS(config, depth):
    printCon(config)                        # print the input

    nodeCnt = 0
    prunNodeCnt = 0;
    for d in range(depth+1):
        print('depth %d',d)
        configHistory = []
        solution = []
        path = []
        #nodeCnt = nodeCnt + DFS(config, configHistory, solution, path, 0, d)
        cnt = DFS(config, configHistory, solution, path, 0, d)
        nodeCnt = nodeCnt + cnt[0]
        prunNodeCnt = prunNodeCnt + cnt[1]
        if len(solution)<1:
            print('no solution')
        else:
            print('solution:')
            for s in solution:
                print(s)
            break
    print('expanded ', nodeCnt, ' nodes')
    print('pruned ', prunNodeCnt, ' nodes')

def checkDuplicate(conHistory, con, depth):
    if len(conHistory) <= depth:
        conHistory.append([])
        return False

    for c in conHistory[depth]:
        if sameConfig(c, con):
            return True
    return False

def antiClock(A):                           # return a matrix anticlockwise rotated by 90 degrees
    R = [[A[x][y] for x in range(len(A))] for y in range(len(A[0])-1, -1, -1)]
    return R

def sameConfig(A,B):                        # check if two configs are same or symmetry in 4 rotations
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

# def checkDuplicate(conHisroty, config):
#     for c in conHisroty:
#         if sameConfig(c, config):
#             return True
#     return False



def YXpath2posPath(config,YXpath):          # change the yx to pos form
    posTable = genPosTable(config)
    posPath = []
    for ft in YXpath:
        newFt = [posTable[ft[0][0]][ft[0][1]],posTable[ft[1][0]][ft[1][1]]]
        posPath.append(newFt)
    return posPath

def checkGoal(config):                      # check if the goal state is reached
    midYX = [int(len(config)/2), int(len(config[0])/2)]
    if config[midYX[0]][midYX[1]] != 'X':
        return False
    for y in range(len(config)):
        for x in range(len(config[0])):
            if (y!= midYX[0] or x != midYX[1]) and config[y][x] == 'X':
                return False
    return True

def avaPeg(config):          # find the pegs that could move
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

def str2List(config):
    l = []
    for str in config:
        row = []
        for letter in str:
            row.append(letter)
        l.append(row)
    return l

def jump(config, curYX, nextYX):                # peg jump from cur to next
    midYX = [int((curYX[0] + nextYX[0])/2),int((curYX[1] + nextYX[1])/2)]
    config[curYX[0]][curYX[1]] = '0'
    config[midYX[0]][midYX[1]] = '0'
    config[nextYX[0]][nextYX[1]] = 'X'

def backTrack(config, curYX, nextYX):           # cancel the jump from cur to next
    midYX = [int((curYX[0] + nextYX[0])/2),int((curYX[1] + nextYX[1])/2)]
    config[curYX[0]][curYX[1]] = 'X'
    config[midYX[0]][midYX[1]] = 'X'
    config[nextYX[0]][nextYX[1]] = '0'

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

def printCon(config):
    print('\nconfigurayion:')
    for c in config:
        print(c)

# def printPosTable(posTable):
#     print('\nposition table:')
#     for t in posTable:
#         print(t)

# def printPegs(pegs, posTable):
#     print('\navalable pegs:')
#     for p in pegs:
#         print('\nfrom',end = " ")
#         print(posTable[p[0][0]][p[0][1]], end = "")
#         print(p[0],end = " to ")
#         for i in range(1,len(p)):
#             print(posTable[p[i][0]][p[i][1]], end = "")
#             print(p[i],end = " ")

# def printHistory(conHistory):
#     for c in conHistory:
#         printCon(c)

# main function
direction = [[-2,0],[0,2],[2,0],[0,-2]]
configutation = ['--000--','--0X0--','00XXX00','000X000','000X000','--000--','--000--']
#configutation = ['--000--','--000--','000X000','0XXXXX0','0000000','--000--','--000--']
depthLimit = 6

start = time.clock()
con = str2List(configutation)
IDS(con, depthLimit)

elapsed = time.clock() - start
print('time used: ',elapsed)
