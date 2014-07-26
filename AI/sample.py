# Representing AI state as a list with the following indices
FUNCTIONS = 0

VARIABLES = 1

GLOBALS = 2
TICKS = 0
HEIGHT = 1
WIDTH = 2

TIMERS = 3
ORIGINAL = 0
CURRENT = 1
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

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

WEIGHTS = (-100000, 0, 10, 1000, 100, -5000)
def depthFirstSearch(x, y, worldMap, currentAIState, depth, lastMove):
    # Since there is no 2x2, depth first search will not have
    # too many problems
    if not depth:
        entity = worldMap[y][x]
        return WEIGHTS[entity]

    childScores = []
    if (y > 0) and (lastMove != DOWN):
        entity = worldMap[y-1][x]
        if entity != WALL:
            score = WEIGHTS[entity]
            childScores.append(depthFirstSearch(x, y-1, worldMap, currentAIState, depth-1, UP))
    if (y + 1 < currentAIState[GLOBALS][HEIGHT]) and (lastMove != UP):
        entity = worldMap[y+1][x]
        if entity != WALL:
            score = WEIGHTS[entity]
            childScores.append(depthFirstSearch(x, y+1, worldMap, currentAIState, depth-1, DOWN))
    if x > 0 and (lastMove != RIGHT):
        entity = worldMap[y][x-1]
        if entity != WALL:
            score = WEIGHTS[entity]
            childScores.append(depthFirstSearch(x-1, y, worldMap, currentAIState, depth-1, LEFT))
    if (x + 1 < currentAIState[GLOBALS][WIDTH]) and (lastMove != LEFT):
        entity = worldMap[y][x-1]
        if entity != WALL:
            score = WEIGHTS[entity]
            childScores.append(depthFirstSearch(x-1, y, worldMap, currentAIState, depth-1, RIGHT))
    if not childScores:
        return (lastMove + 2) % 4
    maxScore = max(childScores)
    minScore = min(childScores)
    if minScore < 0:
        return minScore
    return maxScore

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
    return currentAIState[:GLOBALS] + [[ticks] + currentAIState[GLOBALS][1:]] + currentAIState[GLOBALS + 1:]

t_Sequence = (lambdaGhostMove, actions, eat, dealWithGhosts,
        checkLambdaWin, checkLambdaLoss, incrementTick)

def makeMove(currentAIState):
    def f(x, y):
        return y(x) 
    return reduce(f, t_Sequence, currentAIState)

def getBestMove(currentAIState, t_currentWorldState, depth):
    worldMap = t_currentWorldState[0]
    t_lambdaStatus = t_currentWorldState[1]
    x, y = t_lambdaStatus[1]
    # Dumb logic, always returns first valid move from the sequence (urdl)
    bestScore = -100000
    bestMove = 0 # If there is no legal move, 0 does not matter
    if y > 0:
        if (worldMap[y-1][x] != WALL):
            score = depthFirstSearch(x, y-1, worldMap, currentAIState, depth, UP)
            if score > bestScore:
                bestScore = score
                bestMove = UP
    if x < currentAIState[GLOBALS][WIDTH] - 1:
        if (worldMap[y][x+1] != WALL):
            score = depthFirstSearch(x+1, y, worldMap, currentAIState, depth, RIGHT)
            if score > bestScore:
                bestScore = score
                bestMove = RIGHT
    if y < currentAIState[GLOBALS][HEIGHT] - 1:
        if (worldMap[y+1][x] != WALL):
            score = depthFirstSearch(x, y+1, worldMap, currentAIState, depth, DOWN)
            if score > bestScore:
                bestScore = score
                bestMove = DOWN
    if x > 0:
        if (worldMap[y][x-1] != WALL):
            score = depthFirstSearch(x-1, y, worldMap, currentAIState, depth, LEFT)
            if score > bestScore:
                bestScore = score
                bestMove = LEFT
    return bestMove

def Main(initialWorldState, undocumented):
    def AIStepFunction(currentAIState, currentWorldState):
        bestMove = getBestMove(currentAIState, currentWorldState, 4)
        currentAIState = makeMove(currentAIState)
        return currentAIState, bestMove

    worldMap, lambdaStatus, ghostStatus, fruitStatus = initialWorldState
    # Store height, width for quicker access
    mapHeight = len(worldMap)
    mapWidth = len(worldMap[0])

    initialAIState = []
    initialAIState.append([]) # Functions should go here
    initialAIState.append([]) # Variables if any

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
