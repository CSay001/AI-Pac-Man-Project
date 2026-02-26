# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()   #get current score
        foodList = newFood.asList()
        if foodList:
            minFoodDist = min([manhattanDistance(newPos, food) for food in foodList])
            score += 10.0 / (minFoodDist + 1)   #gives a higher score to the food that is closer to the pacman
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            ghostDist = manhattanDistance(newPos, ghostPos)
            if ghostDist < 2:
                score -= 500   #avoid active ghosts
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:   #self.depth=maximum depth
                return self.evaluationFunction(gameState)   #returns the state's evaluation score
            numAgents = gameState.getNumAgents()
            if agentIndex == 0:   #if agent is pacman then: Pacman's turn (maximizing)
                maxValue = float('-inf')   #we initialize maxValue to negative infinity so that any actual game value will be larger (updates later, as we find better pacman moves)
                legalActions = gameState.getLegalActions(agentIndex)
                for action in legalActions:
                    successor = gameState.generateSuccessor(agentIndex, action)   #new games state after pacman's action
                    value = minimax(1, depth, successor)   #returns the value after all ghosts' action/recursive call to evaluate this successor state/(1 [pass control to ghost 1], depth [stays the same], successor [the new state])
                    maxValue = max(maxValue, value)   #compare value with maxValue and keep the maximum (cause pacman wants to "maximize")
                return maxValue
            else:   #if agent is NOT pacman then: Ghost's turn (minimizing) (aka ghosts want to minimize pacman's score)
                minValue = float('inf')   #we initialize maxValue to POSITIVE infinity so that any actual game value will be SMALLER (updates later, as we find WORSE pacman moves)
                legalActions = gameState.getLegalActions(agentIndex)
                for action in legalActions:
                    successor = gameState.generateSuccessor(agentIndex, action)
                    if agentIndex == numAgents - 1:   #if this is the last ghost, increase depth and go back to pacman
                        value = minimax(0, depth + 1, successor)
                    else:
                        value = minimax(agentIndex + 1, depth, successor)
                    minValue = min(minValue, value)
                return minValue

        #getting the best action for pacman at root
        legalActions = gameState.getLegalActions(0)   #0 is pacman's index
        bestAction = None   #initialize variable to store the best action as "none" (updates later, when we find better values)
        bestValue = float('-inf')   #initialize bestValue to negative infinity so the 1st action we evaluate will be better than this and also always find at least one action to choose
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = minimax(1, 0, successor)   #get number for this action
            if value > bestValue:
                bestValue = value
                bestAction = action   #remember the action
        return bestAction   #return action (not number) (in the recursive call we get number since it returns values)

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alphabeta(agentIndex, depth, gameState, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            numAgents = gameState.getNumAgents()
            if agentIndex == 0:
                maxValue = float('-inf')
                legalActions = gameState.getLegalActions(agentIndex)
                for action in legalActions:
                    successor = gameState.generateSuccessor(agentIndex, action)
                    value = alphabeta(1, depth, successor, alpha, beta)
                    maxValue = max(maxValue, value)
                    if maxValue > beta:   #we don't prune on equality
                        return maxValue  # Prune - no need to check further
                    alpha = max(alpha, maxValue)
                return maxValue
            else:
                minValue = float('inf')
                legalActions = gameState.getLegalActions(agentIndex)
                for action in legalActions:
                    successor = gameState.generateSuccessor(agentIndex, action)
                    if agentIndex == numAgents - 1:
                        value = alphabeta(0, depth + 1, successor, alpha, beta)
                    else:
                        value = alphabeta(agentIndex + 1, depth, successor, alpha, beta)
                    minValue = min(minValue, value)
                    if minValue < alpha:   #we don't prune on equality
                        return minValue  # Prune - no need to check further
                    beta = min(beta, minValue)
                return minValue

        #getting the best action for pacman at root
        legalActions = gameState.getLegalActions(0)
        bestAction = None
        bestValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = alphabeta(1, 0, successor, alpha, beta)   #alphabeta(1,0,-inf,+inf)
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, value)
        return bestAction

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            numAgents = gameState.getNumAgents()
            if agentIndex == 0:
                maxValue = float('-inf')
                legalActions = gameState.getLegalActions(agentIndex)
                for action in legalActions:
                    successor = gameState.generateSuccessor(agentIndex, action)
                    value = expectimax(1, depth, successor)
                    maxValue = max(maxValue, value)
                return maxValue
            else:   # Ghost's turn (expectation over uniform random actions)
                legalActions = gameState.getLegalActions(agentIndex)
                if len(legalActions) == 0:   #we do this to avoid dividing by zero later
                    return self.evaluationFunction(gameState)
                expectedValue = 0
                probability = 1.0 / len(legalActions)
                for action in legalActions:
                    successor = gameState.generateSuccessor(agentIndex, action)
                    if agentIndex == numAgents - 1:
                        value = expectimax(0, depth + 1, successor)
                    else:
                        value = expectimax(agentIndex + 1, depth, successor)
                    expectedValue += probability * value
                return expectedValue

        #getting the best action for pacman at root
        legalActions = gameState.getLegalActions(0)
        bestAction = None
        bestValue = float('-inf')
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = expectimax(1, 0, successor)
            if value > bestValue:
                bestValue = value
                bestAction = action
        return bestAction

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score = currentGameState.getScore()
    foodList = food.asList()
    if foodList:
        minFoodDist = min([manhattanDistance(pos, foodPos) for foodPos in foodList])
        score += 10.0 / (minFoodDist + 1)
    score -= 4 * len(foodList)   #negative score for remaining food
    for i, ghostState in enumerate(ghostStates):   #include ghost states
        ghostPos = ghostState.getPosition()
        ghostDist = manhattanDistance(pos, ghostPos)
        if scaredTimes[i] > 0:
            if ghostDist > 0:
                score += 200.0 / ghostDist   #chasing scared ghosts
        else:
            if ghostDist > 0:   #avoiding active ghosts
                if ghostDist < 3:
                    score -= 200 / (ghostDist + 1)
                else:
                    score -= 10 / (ghostDist + 1)
    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
