def getNewPosition(oldPos, direction):
    if direction == 0: #up
        return (oldPos[0], oldPos[1] - 1)
    if direction == 2: #down
        return (oldPos[0], oldPos[1] - 1)
    if direction == 1: #right
        return (oldPos[0] + 1, oldPos[1])
    return (oldPos[0] - 1, oldPos[1])

def fruit1Valid(ticks):
    return 127 * 200 <= ticks < 127 * 280

def fruit2Valid(ticks):
    return 127 * 400 <= ticks < 127 * 480


######## Sequence in which map should be updated ######
def lambdaGhostMove():
    pass

def actions():
    pass

def eat():
    pass

def dealWithGhosts():
    pass

def checkLambdaWin():
    pass

def checkLambdaLoss():
    pass

def incrementTick():
    pass

Sequence = (lambdaGhostMove, actions, eat, dealWithGhosts,
        checkLambdaWin, checkLambdaLoss, incrementTick)

# Representing AI state as a list with the following indices
TICKS = 0
HEIGHT = 1
WIDTH = 2

# Map Encoding
WALL = 0
EMPTY = 1
PILL = 2
POWERPILL = 3
FRUIT = 4
LAMBDAMAN = 5
GHOST = 6

def parse(worldMap):
    ret = []
    lambdaPos = None
    for y in range(len(worldMap)):
        for x in range(len(worldMap[0])):
            if worldMap[y][x] == LAMBDAMAN:
                lambdaPos = (x, y) # No break, also need to change loops
    ret.append(lambdaPos)
    return ret
            
            
def getBestMove(currentAIState, currentWorldState):
    worldMap = currentWorldState[0]
    parsedMap = parse(worldMap)
    lambdaPos = parsedMap[0]
    x, y = lambdaPos
    # Dumb logic, always returns first valid move from the sequence (urdl)
    if y > 0:
        if worldMap[y-1][x] != 0:
            return 0
    if x < currentAIState[2] - 1:
        if worldMap[y][x+1] != 0:
            return 1
    if y < currentAIState[1] - 1:
        if worldMap[y+1][x] != 0:
            return 2
    return 3 # Illegal move if any, over here is not our problem

def Main(initialWorldState, undocumented):
    def AIStepFunction(currentAIState, currentWorldState):
        bestMove = getBestMove(currentAIState, currentWorldState)
        currentAIState[0] += 1
        return currentAIState, bestMove

    worldMap, lambdaStatus, ghostStatus, fruitStatus = initialWorldState
    # Store height, width for quicker access
    mapHeight = len(worldMap)
    mapWidth = len(worldMap[0])

    initialAIState = []
    initialAIState.append(0) # No ticks so far
    initialAIState.append(mapHeight)
    initialAIState.append(mapWidth)
    
    return initialAIState, AIStepFunction

if __name__ == '__main__':
    worldMap = [[0, 0, 0], [0, 2, 5]]
    initialWorldState = [worldMap, None, None, None]
    initialAIState, AIStepFunction = Main(initialWorldState, None)
    print AIStepFunction(initialAIState, initialWorldState)
