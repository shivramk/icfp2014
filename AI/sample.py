# Representing AI state as a list with the following indices
FUNCTIONS = 0

GLOBALS = 1
TICKS = 0
HEIGHT = 1
WIDTH = 2

TIMERS = 2
LAMBDATICKSTIMER = 0
LAMBDAEATTIMER = 1
GHOST1TICKSTIMER = 2
GHOST2TICKSTIMER = 3
GHOST3TICKSTIMER = 4
GHOST4TICKSTIMER = 5
GHOST1FRIGHTTIMER = 6
GHOST2FRIGHTTIMER = 7
GHOST3FRIGHTTIMER = 8
GHOST4FRIGHTTIMER = 9

# Map Encoding
WALL = 0
EMPTY = 1
PILL = 2
POWERPILL = 3
FRUIT = 4
LAMBDAMAN = 5
GHOST = 6
LAMBDAGHOST = 7


def getNewPosition(oldPos, direction):
    if direction == 0: #up
        return (oldPos[0], oldPos[1] - 1)
    if direction == 2: #down
        return (oldPos[0], oldPos[1] - 1)
    if direction == 1: #right
        return (oldPos[0] + 1, oldPos[1])
    return (oldPos[0] - 1, oldPos[1])

"""
def fruit1Valid(ticks):
    return 127 * 200 <= ticks < 127 * 280

def fruit2Valid(ticks):
    return 127 * 400 <= ticks < 127 * 480
"""

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
    ticks = currentAIState[GLOBALS][TICKS] + 1
    return [ticks] + currentAIState[1:]

t_Sequence = (lambdaGhostMove, actions, eat, dealWithGhosts,
        checkLambdaWin, checkLambdaLoss, incrementTick)

def makeMove(currentAIState):
    def f(x, y):
        return y(x) 
    return reduce(f, t_Sequence, currentAIState)

def getBestMove(currentAIState, t_currentWorldState):
    worldMap = t_currentWorldState[0]
    t_lambdaStatus = t_currentWorldState[1]
    print t_currentWorldState
    x, y = t_lambdaStatus[1]
    # Dumb logic, always returns first valid move from the sequence (urdl)
    legal = 0
    if y > 0:
        if (worldMap[y-1][x] != WALL):
            legal = 0
            if (worldMap[y-1][x] != GHOST):
                return 0
    if x < currentAIState[GLOBALS][WIDTH] - 1:
        if (worldMap[y][x+1] != WALL):
            legal = 1
            if (worldMap[y][x+1] != GHOST):
                return 1
    if y < currentAIState[GLOBALS][HEIGHT] - 1:
        if (worldMap[y+1][x] != WALL):
            legal = 2
            if (worldMap[y+1][x] != GHOST):
                return 2
    if x > 0:
        if (worldMap[y][x-1] != WALL):
            legal = 3
            if (worldMap[y][x-1] != GHOST):
                return 3
    return legal # Illegal move, not sure what to return

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
    initialAIState.append([]) # Functions should go here

    initialAIState.append([])
    initialAIState[GLOBALS].append(0) # No ticks so far
    initialAIState[GLOBALS].append(mapHeight)
    initialAIState[GLOBALS].append(mapWidth)

    initialAIState.append([])
    initialAIState[TIMERS].append(127) # Lambda timer
    initialAIState[TIMERS].append(137) # Lambda eating timer
    initialAIState[TIMERS].append(130) # Ghost 1 timer
    initialAIState[TIMERS].append(132) # Ghost 2 timer
    initialAIState[TIMERS].append(134) # Ghost 3 timer
    initialAIState[TIMERS].append(136) # Ghost 4 timer
    initialAIState[TIMERS].append(195) # Ghost 1 fright
    initialAIState[TIMERS].append(198) # Ghost 2 fright
    initialAIState[TIMERS].append(201) # Ghost 3 fright
    initialAIState[TIMERS].append(204) # Ghost 4 fright
    
    return initialAIState, AIStepFunction

if __name__ == '__main__':
    worldMap = [[0, 0, 0], [0, 2, 5]]
    t_initialWorldState = (worldMap, (0, (2, 1)), None, None)
    initialAIState, AIStepFunction = Main(t_initialWorldState, None)
    currentAIState, bestMove = AIStepFunction(initialAIState, t_initialWorldState)
    print currentAIState, bestMove
