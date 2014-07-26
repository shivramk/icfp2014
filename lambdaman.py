def getBestMove(currentAIState, t_currentWorldState):
    worldMap = t_currentWorldState[0]
    t_lambdaStatus = t_currentWorldState[1]
    # print t_currentWorldState
    height = len(worldMap)
    width = len(worldMap[0])
    x, y = t_lambdaStatus[1]
    # Dumb logic, always returns first valid move from the sequence (urdl)
    legal = 0
    if y > 0:
        if (worldMap[y-1][x] != 0):
            legal = 0
            if (worldMap[y-1][x] != 6):
                return 0
    if x < width - 1:
        if (worldMap[y][x+1] != 0):
            legal = 1
            if (worldMap[y][x+1] != 6):
                return 1
    if y < height - 1:
        if (worldMap[y+1][x] != 0):
            legal = 2
            if (worldMap[y+1][x] != 6):
                return 2
    if x > 0:
        if (worldMap[y][x-1] != 0):
            legal = 3
            if (worldMap[y][x-1] != 6):
                return 3
    return legal # Illegal move, not sure what to return

def AIStepFunction(currentAIState, t_currentWorldState):
    return currentAIState, getBestMove(currentAIState, t_initialWorldState)

def Main(initialWorldState, undocumented):
    return 0, AIStepFunction
