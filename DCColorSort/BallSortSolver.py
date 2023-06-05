import pygame
import time
import json
import os

import BallSortBack
from binary_heap import BinaryHeap
from node import Node
import heuristics

HEURISTIC_PONDERATOR = 1
VISUALIZATION = True
MOVING_SPEED = 15

# Replace with the map to be tested
GAME_MAP = "map_15"

# Compute the map's absolute path
relative_map_path = os.path.join("maps", f"{GAME_MAP}.json")
current_path = os.path.dirname(os.path.realpath(__file__))
MAP_PATH = os.path.join(current_path, relative_map_path)

# Load the map's data
with open(MAP_PATH, 'r') as f:
    MAP_DATA = json.load(f)

class AStarSolver():

    '''
        This class models the solver for the game and performs the A* algorithm in order to find a solution for it.
    '''

    def __init__(self, heuristic = heuristics.no_heuristic, visualization = VISUALIZATION, map_info = MAP_DATA):

        '''
            Parameters:
                heuristic (function) : function used as heuristic for the search (should take a State as an input and output a number), no heuristic by default.
                visualization (bool) : whether to or not to display the solution after it's found.

        '''

        self.expansions = 0
        self.generated = 0
        self.memory = 0
        self.start_time = time.time()

        # Load the map's data
        self.game = BallSortBack.BallSortGame()
        self.game.load_map(map_info)
        self.initial_state = self.game.init_state

        self.heuristic = heuristic
        self.open = BinaryHeap()

        if visualization:
            self.game.start_visualization(text = "Solving...")
    
    def __init__(self, heuristic = heuristics.no_heuristic, visualization = VISUALIZATION, map_info = MAP_DATA):
        '''
            Parameters:
                heuristic (function) : function used as heuristic for the search (should take a State as an input and output a number), no heuristic by default.
                visualization (bool) : whether to or not to display the solution after it's found.
        '''

        self.expansions = 0
        self.generated = 0
        self.memory = 0
        self.start_time = time.time()

        # Load the map's data
        self.game = BallSortBack.BallSortGame()
        self.game.load_map(map_info)
        self.initial_state = self.game.init_state

        self.heuristic = heuristic
        self.open = BinaryHeap()

        if visualization:
            self.game.start_visualization(text = "Solving...")
    
    def search(self):
        '''
        Performs the A* search for a solution.
        '''
        print("Computing...")

        ABIERTOS = BinaryHeap()  # Open list represented as a binary heap
        ABIERTOS_DICT = {}  # Open list represented as a dictionary
        CERRADOS = {}  # Closed list represented as a dictionary
        INITIAL = Node(self.initial_state)  # Initial node
        INITIAL.g = 0  # cost to reach the initial state
        INITIAL.h = self.heuristic(self.initial_state)  # heuristic value for the initial state
        INITIAL.key = INITIAL.g + INITIAL.h  # set the key as its priority
        ABIERTOS.insert(INITIAL)  # insert the initial node into the heap
        ABIERTOS_DICT[INITIAL.state] = INITIAL  # insert the initial node into the dictionary

        self.memory += 1
        self.generated += 1

        while not ABIERTOS.is_empty():
            MEJORNODO = ABIERTOS.extract()  # extract the node with minimum key
            ABIERTOS_DICT[MEJORNODO.state]  # delete the node from the dictionary
            CERRADOS[MEJORNODO.state] = MEJORNODO  # add this node to the closed list

            self.memory = len(ABIERTOS_DICT) + len(CERRADOS)  # update the memory usage

            # if this node is the goal state, reconstruct the path and return it
            if self.heuristic(MEJORNODO.state) == 0:
                path, actions = MEJORNODO.trace()  # Reconstruct path using the trace function
                self.end_time = time.time()
                return actions, path

            self.game.current_state = MEJORNODO.state  # update the game's current state

            SUCESORES = self.game.get_valid_moves()  # generate successors
            self.expansions += 1
            for new_state, move, _ in SUCESORES:  # unpacking the return value of get_valid_moves()
                state = new_state  # convert the new_state to a list of lists
                SUCESOR = Node(state, MEJORNODO, [move])
                SUCESOR.g = MEJORNODO.g + 1  # cost of the path to the successor
                SUCESOR.h = self.heuristic(state)  # heuristic value for the successor
                SUCESOR.key = SUCESOR.g + SUCESOR.h  # set the key as its priority

                self.generated += 1

                # if the successor is in the closed list
                if SUCESOR.state in CERRADOS:
                    VIEJO = CERRADOS[SUCESOR.state]  # get the old version of the successor
                    if SUCESOR.g < VIEJO.g:  # we found a better path
                        VIEJO.parent = MEJORNODO  # update the parent
                        VIEJO.g = SUCESOR.g  # update g
                        VIEJO.key = SUCESOR.key  # update key
                        ABIERTOS.insert(VIEJO)  # update the node in the heap
                        ABIERTOS_DICT[SUCESOR.state] = VIEJO  # update the node in the dictionary

                # if the successor is in the open list
                elif not ABIERTOS.is_empty() and ABIERTOS.contains(SUCESOR):
                    VIEJO = ABIERTOS_DICT.get(SUCESOR.state, None)  # get the old version of the successor
                    if VIEJO:
                        if SUCESOR.g < VIEJO.g:  # we found a better path
                            VIEJO.parent = MEJORNODO  # update the parent
                            VIEJO.g = SUCESOR.g  # update g
                            VIEJO.key = SUCESOR.key  # update key
                            ABIERTOS.insert(VIEJO)  # update the node in the heap
                            ABIERTOS_DICT[SUCESOR.state] = VIEJO  # update the node in the dictionary

                # if the successor is not in open list and not in closed list
                else:
                    ABIERTOS.insert(SUCESOR)  # insert the successor into the heap
                    ABIERTOS_DICT[SUCESOR.state] = SUCESOR  # insert the successor into the dictionary

        # If no solution was found, return None.
        return None
    
    def lazysearch(self):
        '''
        Performs the A* search for a solution.
        '''
        print("Computing...")

        ABIERTOS = BinaryHeap()  # Open list represented as a binary heap
        CERRADOS = {}  # Closed list represented as a dictionary
        INITIAL = Node(self.initial_state)  # Initial node
        INITIAL.g = 0  # cost to reach the initial state
        INITIAL.h = self.heuristic(self.initial_state)  # heuristic value for the initial state
        INITIAL.key = INITIAL.g + INITIAL.h  # set the key as its priority
        ABIERTOS.insert(INITIAL)  # insert the initial node into the heap

        self.memory += 1
        self.generated += 1

        while not ABIERTOS.is_empty():
            MEJORNODO = ABIERTOS.extract()  # extract the node with minimum key
            CERRADOS[MEJORNODO.state] = MEJORNODO  # add this node to the closed list

            self.memory = max(self.memory, ABIERTOS.size + len(CERRADOS))

            # if this node is the goal state, reconstruct the path and return it
            if self.heuristic(MEJORNODO.state) == 0:
                path, actions = MEJORNODO.trace()  # Reconstruct path using the trace function
                self.end_time = time.time()
                return actions, path

            self.game.current_state = MEJORNODO.state  # update the game's current state

            SUCESORES = self.game.get_valid_moves()  # generate successors
            self.expansions += 1
            for new_state, move, _ in SUCESORES:  # unpacking the return value of get_valid_moves()
                state = new_state  # convert the new_state to a list of lists
                SUCESOR = Node(state, MEJORNODO, [move])
                SUCESOR.g = MEJORNODO.g + 1  # cost of the path to the successor
                SUCESOR.h = self.heuristic(state)  # heuristic value for the successor
                SUCESOR.key = SUCESOR.g + SUCESOR.h  # set the key as its priority
                self.generated += 1
                ABIERTOS.insert(SUCESOR)  # insert the successor into the heap

        # If no solution was found, return None.
        return None

    def greedysearch(self): #  Greedy Best First Search
        '''
        Performs the Best First Search search for a solution.
        '''
        print("Computing...")

        ABIERTOS = BinaryHeap()  # Open list represented as a binary heap
        CERRADOS = {}  # Closed list represented as a dictionary
        INITIAL = Node(self.initial_state)  # Initial node
        INITIAL.g = 0  # cost to reach the initial state
        INITIAL.h = self.heuristic(self.initial_state)  # heuristic value for the initial state
        INITIAL.key = INITIAL.h  # set the key as its priority
        ABIERTOS.insert(INITIAL)  # insert the initial node into the heap

        self.memory += 1
        self.generated += 1

        while not ABIERTOS.is_empty():
            MEJORNODO = ABIERTOS.extract()  # extract the node with minimum key
            CERRADOS[MEJORNODO.state] = MEJORNODO  # add this node to the closed list

            self.memory = max(self.memory, ABIERTOS.size + len(CERRADOS))

            # if this node is the goal state, reconstruct the path and return it
            if self.heuristic(MEJORNODO.state) == 0:
                path, actions = MEJORNODO.trace()  # Reconstruct path using the trace function
                self.end_time = time.time()
                return actions, path

            self.game.current_state = MEJORNODO.state  # update the game's current state

            SUCESORES = self.game.get_valid_moves()  # generate successors
            self.expansions += 1
            for new_state, move, _ in SUCESORES:  # unpacking the return value of get_valid_moves()
                state = new_state  # convert the new_state to a list of lists
                SUCESOR = Node(state, MEJORNODO, [move])
                SUCESOR.g = MEJORNODO.g + 1  # cost of the path to the successor
                SUCESOR.h = self.heuristic(state)  # heuristic value for the successor
                SUCESOR.key = SUCESOR.h  # set the key as its priority
                self.generated += 1
                ABIERTOS.insert(SUCESOR)  # insert the successor into the heap

        # If no solution was found, return None.
        return None


    
    def _reconstruct_path(self, current_node):
        '''Reconstruct the path from the start state to the current (goal) state.'''
        path, actions = current_node.trace()
        return path, actions

        
if __name__ == "__main__":
    # We create an instance for the solver and perform the search on the current map
    solver = AStarSolver(heuristic = heuristics.wagdy_heuristic, visualization = VISUALIZATION)
    sol = solver.greedysearch()
    actions = sol[0]
    path = sol[1]

    # In case a solution was found, try it out
    if sol[0] is not None:
        solver.game.current_state = solver.game.init_state
        for step in actions:
          
            solver.game.make_move(step[0][0], step[0][1], moving_speed = MOVING_SPEED)

        if VISUALIZATION:
            solver.game.front.draw(solver.game.current_state, text = ":)")
            pygame.time.wait(1000) 
            pygame.quit()

        print("The search was succesful at finding a solution.")
        print(f"The number of expansions: {solver.expansions}")
        print(f"The time it took to find a solution: {solver.end_time - solver.start_time}")
        print(f"The memory used: {solver.memory}")
        print(f"Number of steps: {len(actions)}")