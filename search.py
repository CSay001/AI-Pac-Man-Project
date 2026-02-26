# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    frontier = util.Stack()
    frontier.push((start, []))
    visited = []
    visited.append(start)
    while frontier.isEmpty()==False:
        state, path = frontier.pop()
        visited.append(state)
        if problem.isGoalState(state):
            print(path)
            return path
        for successor in problem.getSuccessors(state):
            next_state = successor[0]
            if next_state not in visited:
                next_path = successor[1]
                new_path=path + [next_path]
                frontier.push((next_state, new_path))
    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    frontier = util.Queue()
    frontier.push((start, []))
    visited = []
    visited.append(start)
    while frontier.isEmpty()==False:
        state, path = frontier.pop()
        if problem.isGoalState(state):
            print(path)
            return path
        for successor in problem.getSuccessors(state):
            next_state = successor[0]  # updating the state
            if next_state not in visited:
                visited.append(next_state)
                next_path = successor[1]  # updating the path
                new_path = path + [next_path]  # adding the new path to the existing one in a list
                frontier.push((next_state, new_path))
    print(new_path)
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start=problem.getStartState()
    visited=[]
    frontier=util.PriorityQueue()
    frontier.push((start, []), 0)
    while frontier.isEmpty()==False:
        state, path = frontier.pop()
        if problem.isGoalState(state):
            print(path)
            return path
        if state not in visited:
            for successor in problem.getSuccessors(state):
                next_state = successor[0]   #updating the state
                if next_state not in visited:
                    next_path = successor[1]   #updating the path
                    new_path = path + [next_path]   #adding the new path to the existing one in a list
                    frontier.push((next_state, new_path), problem.getCostOfActions(new_path))
        visited.append(state)
    print(new_path)
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start=problem.getStartState()
    frontier=util.PriorityQueue()
    frontier.push((start, [], 0), heuristic(start, problem))   #(state, path, g cost)
    cheap_g={start: 0}   #stores the cheapest g cost up until now to reach a certain state

    while frontier.isEmpty()==False:
        state, path, g = frontier.pop()
        if state in cheap_g and g>cheap_g[state]:
            continue
        if problem.isGoalState(state):
            print(path)
            return path
        cheap_g[state]=g  #adding the state with it's cheapest g in the list
        for next_state, action, successor_cost in problem.getSuccessors(state):
            next_g=g+successor_cost
            if next_state not in cheap_g or next_g<cheap_g[next_state]:
                cheap_g[next_state]=next_g   #udpating dictionary
                next_path=path+[action]   #adding the new path to the existing one in a list
                f=next_g + heuristic(next_state, problem)   #we use heuristic(state.problem) whenever we need to estimate the remaining cost
                frontier.push((next_state, next_path, next_g), f)   #adding to the frontier the next tuple of state,path,g according to the priority number f
    print(next_path)
    return []
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
