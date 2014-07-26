# Representing AI state as a list with the following indices
TICKS = 0
SCORE = 1
HEIGHT = 2
WIDTH = 3

# Map Encoding
WALL = 0
EMPTY = 1
PILL = 2
POWERPILL = 3
FRUIT = 4
LAMBDAMAN = 5
GHOST = 6


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
def lambdaGhostMove(currentAIState):
    return currentAIState

def actions(currentAIState):
    return currentAIState

def eat(currentAIState):
    return currentAIState

def dealWithGhosts(currentAIState):
    return currentAIState

def checkLambdaWin(currentAIState):
    return currentAIState

def checkLambdaLoss(currentAIState):
    return currentAIState

def incrementTick(currentAIState):
    ticks = currentAIState[TICKS] + 1
    return [ticks] + currentAIState[1:]

Sequence = (lambdaGhostMove, actions, eat, dealWithGhosts,
        checkLambdaWin, checkLambdaLoss, incrementTick)

def makeMove(currentAIState):
    def f(x, y):
        return y(x) 
    return reduce(f, Sequence, currentAIState)

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
    lambdaStatus = currentWorldState[1]
    x, y = lambdaStatus[1]
    # Dumb logic, always returns first valid move from the sequence (urdl)
    if y > 0:
        if worldMap[y-1][x] != 0:
            return 0
    if x < currentAIState[WIDTH] - 1:
        if worldMap[y][x+1] != 0:
            return 1
    if y < currentAIState[HEIGHT] - 1:
        if worldMap[y+1][x] != 0:
            return 2
    return 3 # Illegal move if any, over here is not our problem

def Main(initialWorldState, undocumented):
    def AIStepFunction(currentAIState, currentWorldState):
        bestMove = getBestMove(currentAIState, currentWorldState)
        currentAIState = makeMove(currentAIState)
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

def getNewMap(oldMap, move):
    # This is dumb and will only consider lambdaman
    # Right now, only used for testing
    newMap = []
    for row in oldMap:
        newMap.append(row[:])
    x, y = parse(oldMap)[0]
    newMap[y][x] = EMPTY
    if move == 0:
        newMap[y-1][x] = LAMBDAMAN
    elif move == 1:
        print newMap, y, x
        newMap[y][x+1] = LAMBDAMAN
    elif move == 2:
        newMap[y+1][x] = LAMBDAMAN
    else:
        newMap[y][x-1] = LAMBDAMAN
    return newMap

if __name__ == '__main__':
    worldMap = [[0, 0, 0], [0, 2, 5]]
    initialWorldState = [worldMap, None, None, None]
    initialAIState, AIStepFunction = Main(initialWorldState, None)
    print initialWorldState, initialAIState
    currentAIState, bestMove = AIStepFunction(initialAIState, initialWorldState)
    currentWorldState = [getNewMap(initialWorldState[0], bestMove)]
    print currentWorldState, currentAIState, bestMove
    currentAIState, bestMove = AIStepFunction(initialAIState, currentWorldState)
    currentWorldState = [getNewMap(currentWorldState[0], bestMove)]
    currentAIState, bestMove = AIStepFunction(initialAIState, currentWorldState)
    print currentWorldState, currentAIState, bestMove

