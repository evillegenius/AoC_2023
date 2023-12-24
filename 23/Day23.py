#!/usr/bin/env python
"""
<Problem description here>
"""
import sys
import os
import re
import numpy as np
import scipy as sp
from collections import namedtuple


class Dir(namedtuple('Dir', 'dr dc')):
    def Rotate(self):
        return Dir(-self[1], self[0])

NORTH = Dir(-1, 0)
SOUTH = Dir(1, 0)
WEST = Dir(0, -1)
EAST = Dir(0, 1)

NOT_NORTH = -1
NOT_SOUTH = -2
NOT_WEST = -3
NOT_EAST = -4

EXCLUDED = {NORTH: NOT_NORTH,
            SOUTH: NOT_SOUTH,
            WEST: NOT_WEST,
            EAST: NOT_EAST}

ROCK = -99

class Pos(namedtuple('Pos', 'row col')):
    def __add__(self, dir):
        return Pos(self[0] + dir[0], self[1] + dir[1])
    
    def __iadd__(self, dir):
        return Pos(self[0] + dir[0], self[1] + dir[1])

    def __sub__(self, rhs):
        return Dir(self[0] - rhs[0], self[1] - rhs[1])
    
    def neighbors(self):
        return ((self.row-1, self.row, self.row, self.row+1),
                (self.col, self.col-1, self.col+1, self.col))

    
class Connection:
    id: int = 0
    def __init__(self, node1, node2, score):
        self.node1 = node1
        self.node2 = node2
        self.score = score
        self.id = Connection.id
        Connection.id += 1

        self.available = bool(self.node1) and bool(self.node2)
        self.traversed = False
        print(repr(self))

    def OtherNode(self, node):
        if node == self.node1: return self.node2
        elif node == self.node2: return self.node1
        else: assert False, "OtherNode called with invalid node"

    def __repr__(self):
        return f'Connection(id={self.id}, {self.node1} -> {self.node2}, score={self.score})'


class Node:
    def __init__(self, pos):
        self.pos = pos
        self.connections = []
        self.available = True
        self.traversed = False
        print(repr(self))

    def __repr__(self):
        return f'Node({self.pos}, connections={self.connections}, available={self.available})'
    
    def __str__(self):
        return f'Node(({self.pos.row}, {self.pos.col}))'

    
class Day23:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

        np.set_printoptions(linewidth=180)


    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day23')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        ########################################################################
        # If the puzzle is not grid/map based, delete these lines.
        gridKey = {'.': 0,
                   '^': NOT_SOUTH,
                   '<': NOT_EAST,
                   'v': NOT_NORTH,
                   '>': NOT_WEST,
                   '#': ROCK}
        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.grid = np.zeros((self.height, self.width), dtype=int)
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                self.grid[row, col] = gridKey[ch]

        if not os.path.isfile(self.input + '.npy'):
            np.save(self.input + ".npy", self.grid)
        #
        ########################################################################

    def Traverse(self, inGrid, pos, dir):
        grid = inGrid.copy()

        paths = [(pos, dir)]
        count = 0

        while len(paths) == 1:
            pos, dir = paths.pop()
            pos += dir
            grid[pos] = 1
            count += 1

            if pos.row == self.height - 1:
                return count

            dir = dir.Rotate()
            gridVal = grid[pos + dir]
            if ROCK < gridVal <= 0 and EXCLUDED[dir] != gridVal:
                paths.append((pos, dir))

            dir = dir.Rotate()
            gridVal = grid[pos + dir]
            if ROCK < gridVal <= 0 and EXCLUDED[dir] != gridVal:
                paths.append((pos, dir))

            dir = dir.Rotate()
            gridVal = grid[pos + dir]
            if ROCK < gridVal <= 0 and EXCLUDED[dir] != gridVal:
                paths.append((pos, dir))

            dir = dir.Rotate()
            gridVal = grid[pos + dir]
            if ROCK < gridVal <= 0 and EXCLUDED[dir] != gridVal:
                paths.append((pos, dir))

        moreSteps = max((self.Traverse(grid, p, d)
                         for p, d in paths), default=0)
        
        return 0 if moreSteps == 0 else count + moreSteps

        
    def Part1(self):
        answer = 0

        grid = self.grid.copy()

        startPos = Pos(0, 1)
        startDir = SOUTH

        grid[startPos] = 1
        
        answer = self.Traverse(grid, startPos, startDir)

        return answer

    def Follow(self, choices, visited, startPos, dir):
        count = 0
        pos = startPos + dir
        visited[pos] = True
        while choices[pos] == 2:
            count += 1
            for dir in (NORTH, SOUTH, EAST, WEST):
                if choices[pos + dir] == 2:
                    if not visited[pos + dir]:
                        # Found the next step.
                        pos += dir
                        visited[pos] = True
                        break
                elif choices[pos + dir] != 0:
                    if pos + dir == startPos:
                        # This is where we started
                        continue

                    pos += dir
                    break
            else:
                # End of the line. This path is a dead end. Create an unavailable
                # connection
                connection = Connection(startNode, None, 0)
                return connection
            
        endPos = pos

        startNode = self.nodes[startPos]
        endNode = self.nodes[endPos]

        connection = Connection(startNode, endNode, count)
        return connection

            
    def Part2(self):
        answer = 0

        # Convert the grid into a set of nodes and connections.
        # Nodes are places where paths intersect. Connections are
        # sections of path without intersections. Connections always
        # have a fixed score and the entire connection can either be
        # traversed or not.
        # Nodes also have a fixed score of 1 and can be traversed or
        # not.
        # Connections and nodes can also become deactivated. If a node
        # is traversed, then the unused connections can never be used.
        #
        # Find the nodes with array manipulation and convolve.

        # self.grid // ROCK yields 1 for rocks and 0 for everything
        # else. 1 - grid inverts that to 1 for paths and 0 for everything else
        grid = 1 - (self.grid // ROCK)

        plus = np.array([[0, 1, 0],
                         [1, 0, 1],
                         [0, 1, 0]])
        
        # Sum the number of move choices available to each grid point and
        # then zero (by multiplication) the results for walls, keeping only
        # the number of choices for each path point.
        choices = sp.signal.convolve2d(grid, plus, mode='same') * grid

        # Choices looks like:
        #
        #  1                     
        #  2222222         222   
        #        2         2 2   
        #    22222 22322   2 2   
        #    2     2 2 2   2 2   
        #    32222 2 2 22222 222 
        #    2   2 2 2         2 
        # ...
        # where 1 is a start or end node, 2 is a simple path, and 3 or 4 is
        # an intersection.  Create nodes for the intersections.

        self.nodes: dict[Pos, Node] = {}
        self.connections: dict[int, Connection] = {}

        nodeLocs = np.argwhere(grid * (choices > 2))
        for nodeLoc in nodeLocs:
            pos = Pos(*nodeLoc)
            self.nodes[pos] = Node(pos)

        nodeLocs = np.argwhere(grid * (choices == 1))
        for nodeLoc in nodeLocs:
            pos = Pos(*nodeLoc)
            self.nodes[pos] = Node(pos)
            if pos.row == 0:
                self.startNode = self.nodes[pos]
            elif pos.row == self.height - 1:
                self.endNode = self.nodes[pos]

        # Everything between the nodes is a single path find them
        visited = np.zeros(grid.shape, dtype=bool)
        for node in self.nodes.values():
            if node is self.startNode or node is self.endNode:
                continue

            visited[node.pos] = True

            for dir in (NORTH, SOUTH, EAST, WEST):
                if not visited[node.pos + dir] and choices[node.pos + dir] == 2:
                    connection = self.Follow(choices, visited, node.pos, dir)

                    self.connections[connection.id] = connection
                    if connection.node1:
                        connection.node1.connections.append(connection)

                    if connection.node2:
                        connection.node2.connections.append(connection)

        # Now there is a much smaller set of things to traverse.

        for nodePos, node in self.nodes.items():
            print(f'{nodePos} -> {node}', end=' ')

            if nodePos.row == 0:
                self.startNode = node
                print('(start)')
            elif nodePos.row == self.height - 1:
                self.endNode = node
                print('(end)')
            else:
                print()

        answer = self.TraverseNodes(self.startNode)
        return answer
    
    def TraverseNodes(self, node):
        assert node.available, f"Node {node!r} is unavailable!"
        if node == self.endNode: return 1

        node.available = False

        # Save the available state of the connections and mark them
        # all unavailable
        availableState = [conn.available for conn in node.connections]
        scores = [0] * len(node.connections)

        for i, conn in enumerate(node.connections):
            conn.available = False

        for i, conn in enumerate(node.connections):
            if not availableState[i]:
                continue
            
            otherNode = conn.OtherNode(node)

            scores[i] += self.TraverseNodes(otherNode)       

        score = max(scores) + 1 # 1 for the node itself

        # Restore the available state
        for i, conn in enumerate(node.connections):
            conn.available = availableState[i]

        node.available = True

        return score

if __name__ == '__main__':
    problem = Day23()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



