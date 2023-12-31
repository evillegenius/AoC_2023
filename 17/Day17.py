#!/usr/bin/env python3
"""
<Problem description here>
"""
import os
import numpy as np
from collections import namedtuple
from dataclasses import dataclass
import itertools
import math

NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

class Pos(namedtuple('Pos', 'row col')):
    pass

NORTH_DIR = Pos(-1,  0)
WEST_DIR  = Pos( 0, -1)
SOUTH_DIR = Pos( 1,  0)
EAST_DIR  = Pos( 0,  1)

class Day17:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day17')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        if os.path.isfile(self.input + ".npy"):
            self.cost = np.load(self.input + ".npy")
            self.height, self.width = self.cost.shape

        else:
            with open(self.input) as input:
                self.lines = input.read().strip().split('\n')

            self.width = len(self.lines[0])
            self.height = len(self.lines)

            self.cost = np.zeros((self.height, self.width), dtype=int)
            for row, line in enumerate(self.lines):
                for col, ch in enumerate(line):
                    self.cost[row, col] = int(ch)

            np.save(self.input + ".npy", self.cost)

        self.huge = 10 ** (math.ceil(math.log10(self.cost.sum()))) - 1


    def NeighborCells(self, row, col, dir, remain):
        if dir == NORTH:
            neighbors = [(row, col-1, WEST, 2),
                         (row, col+1, EAST, 2),
                         (row-1, col, NORTH, remain-1)]
        elif dir == WEST:
            neighbors = [(row-1, col, NORTH, 2),
                         (row+1, col, SOUTH, 2),
                         (row, col-1, WEST, remain-1)]
        elif dir == SOUTH:
            neighbors = [(row, col+1, EAST, 2),
                         (row, col-1, WEST, 2),
                         (row+1, col, SOUTH, remain-1)]
        elif dir == EAST:
            neighbors = [(row+1, col, SOUTH, 2),
                         (row-1, col, NORTH, 2),
                         (row, col+1, EAST, remain-1)]
        else:
            assert False, "Unknown dir: {dir!r}"

        neighbors = [n
                     for n in neighbors
                     if (n[3] >= 0 and 
                         0 <= n[0] < self.height and
                         0 <= n[1] < self.width)]

        # Transpost the neighbors from
        #    ((r, c, d, x),
        #     (r, c, d, x))
        # to
        #    ((r,r), (c,c), (d,d), (x,x))
        indices = (tuple(n[0] for n in neighbors),
                   tuple(n[1] for n in neighbors),
                   tuple(n[2] for n in neighbors),
                   tuple(n[3] for n in neighbors))
        
        return indices


    def Part1(self):
        answer = 0
        # Dynamic-ish programming solution. There doesn't seem to be a solution
        # that computes all the sub-answers before computing an answer for a
        # given state. So we iterate until it settles down. :-/

        score = np.full((self.height, self.width, 4, 3), self.huge, dtype=int)
        score[-1, -1] = self.cost[-1, -1]  # broadcast to all 12 states

        skip = (self.height - 1) + (self.width - 1)
        count = 0
        while True:
            count += 1
            prevScore = score.copy()
            for x in (0, 1, 2):
                for d in (NORTH, WEST, SOUTH, EAST):
                    for r in reversed(range(self.height)):
                        for c in reversed(range(self.width)):
                            if r + c == skip:
                                continue
                            indices = self.NeighborCells(r, c, d, x)
                            score[r, c, d, x] = score[indices].min() + self.cost[r, c]
            if np.array_equal(prevScore, score):
                break

            if count % 100 == 0:
                print(f'{count} iterations...')

            assert count < 10000

        # changed = 1
        # while changed:
        #     changed = 0
        #     diag = self.height + self.width

        answer = score[0, 0, 0, 0] - self.cost[0, 0]
        return answer

    def Part2(self):
        # Ok, pseudo dynamic programming did not work that great. Try Dijkstra's
        # algorithm for part 2.
        #
        # queue.PriorityQueue looks like it has too much baggage and does not
        # allow you to adjust the priority of an item.
        #
        import heapq

        class PriorityQueue:
            """
            Priority queue that lets you adjust the priority of a queued item.
            Neither queue.PriorityQueue nor heapq allow you to do so directly.
            Queue items must be hashable (i.e., immutable) and ordered.
            """
            def __init__(self):
                self.heap = []
                self.map = {}

            def __len__(self):
                return len(self.heap)

            def Push(self, item, priority):
                """
                Push an item on the queue. If it was already there, adjust
                its priority.
                """
                if item in self.map:
                    self.map[item][0] = priority
                    heapq.heapify(self.heap)
                else:
                    heapItem = [priority, item]
                    self.map[item] = heapItem
                    heapq.heappush(self.heap, heapItem)

            def Pop(self):
                priority, item = heapq.heappop(self.heap)
                del self.map[item]
                return (item, priority)

        Item = namedtuple('Item', 'row col heading steps')

        pending = PriorityQueue()

        # Shape is designed so scores can be indexed by Item instances
        shape = self.cost.shape + (4, 11)
        scores = np.full(shape, self.huge, dtype=np.int32)

        pending.Push(Item(0, 0, EAST, 0), 0)
        pending.Push(Item(0, 0, SOUTH, 0), 0)

        def GoStraight(item):
            row, col, heading, steps = item
            if   heading == NORTH: dr, dc = NORTH_DIR
            elif heading == WEST:  dr, dc = WEST_DIR
            elif heading == SOUTH: dr, dc = SOUTH_DIR
            elif heading == EAST:  dr, dc = EAST_DIR
            else:
                assert False, f"Unknown heading: {heading!r}"

            advance = max(1, 4 - steps)
            # Make sure we won't step off the edge of the world
            testRow = row + dr * advance
            testCol = col + dc * advance
            if 0 <= testRow < self.height and 0 <= testCol < self.width:
                return Item(row + dr, col + dc, heading, steps + 1)
            
            return None

        def TurnLeft(item):
            return GoStraight(item._replace(heading=(item.heading + 1) % 4, steps=0))
        
        def TurnRight(item):
            return GoStraight(item._replace(heading=(item.heading - 1) % 4, steps=0))

        targetPos = (self.height - 1, self.width - 1)
        while pending:
            item, score = pending.Pop()
            row, col, heading, steps = item

            if (row, col) == targetPos and steps > 3:
                answer = score
                break

            neighbors = []
            if steps > 3:
                # We can turn
                if leftNeighbor := TurnLeft(item):
                    neighbors.append(leftNeighbor)
                if rightNeighbor := TurnRight(item):
                    neighbors.append(rightNeighbor)
            if steps < 10:
                # We can go straight
                if aheadNeighbor := GoStraight(item):
                    neighbors.append(aheadNeighbor)

            for neighbor in neighbors:
                # An Item like neighbor starts with a row and column, so
                # neighbor[:2] indexes nicely into self.cost.
                newScore = score + self.cost[neighbor[:2]]
                if newScore < scores[neighbor]:
                    scores[neighbor] = newScore
                    # Note: if neighbor is already queued, Push will just
                    # reprioritize it with newScore
                    pending.Push(neighbor, newScore)

        return answer
    
if __name__ == '__main__':
    problem = Day17()
    
    # answer1 = problem.Part1()
    # print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



