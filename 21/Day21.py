#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import numpy as np
from collections import namedtuple

class Pos(namedtuple('Pos', 'row col')):
    pass

class Day21:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day21')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.grid = np.zeros((self.height, self.width), dtype=int)

        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                # empty == 0, rock == 1, start == 2
                self.grid[row, col] = '.#S'.find(ch)

        self.startPos = Pos(*(np.argwhere(self.grid == 2)[0]))
        np.save('grid.npy', self.grid)

    def Part1(self):
        answer = 0

        rocks = self.grid.copy()

        rocks *= 1000  # empty space is 0, rock is 1000
        rocks -= 1     # empty space is -1, rock is 999
        rocks[self.startPos] = 0  # start is 0 steps

        grid = np.full((self.width, self.height), -1, dtype=int)
        grid[self.startPos] = 0  # start is 0 steps

        print(f'startPos = {self.startPos}')

        steps = 64

        for step in range(steps):
            locs = np.argwhere(grid == step)
            for loc in locs:
                if loc[0] < self.height-1:
                    grid[loc[0] + 1, loc[1]] = step + 1
                if loc[0] > 0:
                    grid[loc[0] - 1, loc[1]] = step + 1
                if loc[1] < self.width-1:
                    grid[loc[0], loc[1] + 1] = step + 1
                if loc[1] > 0:
                    grid[loc[0], loc[1] - 1] = step + 1

            np.maximum(grid, rocks, out=grid)
            # self.PrintGrid(grid, step + 1)


        answer = np.count_nonzero(grid == steps)
        return answer

    def PrintGrid(self, grid, steps):
        print(f'After step {steps}: {np.count_nonzero(grid == steps)} possibilities')
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                cell = grid[row, col]
                if cell == 9999:
                    print('x', end='')
                elif cell == steps:
                    print('O', end='')
                else:
                    print('.', end='')
            print()

        print('', flush=True)

    def Part2(self):
        answer = 0
        rocks = self.grid.copy()
        rocks *= 10000  # empty space is 0, rock is 10000
        rocks -= 1      # empty space is -1, rock is 9999
        rocks[self.startPos] = 0  # start is 0 steps
        rocks = np.tile(rocks, (5, 5))

        height, width = rocks.shape

        self.startPos = (self.startPos[0] + 2 * self.height,
                         self.startPos[1] + 2 * self.width)

        grid = np.full(rocks.shape, -1, dtype=int)
        grid[self.startPos] = 0  # start is 0 steps

        print(f'startPos = {self.startPos}')

        steps = 65 + 2 * 131

        for step in range(steps):
            locs = np.argwhere(grid == step)
            for loc in locs:
                if loc[0] < height-1:
                    grid[loc[0] + 1, loc[1]] = step + 1
                if loc[0] > 0:
                    grid[loc[0] - 1, loc[1]] = step + 1
                if loc[1] < width-1:
                    grid[loc[0], loc[1] + 1] = step + 1
                if loc[1] > 0:
                    grid[loc[0], loc[1] - 1] = step + 1

            np.maximum(grid, rocks, out=grid)
        # self.PrintGrid(grid, step + 1)

        # Summarize the 131 square blocks into counts
        counts = np.zeros((5,5), dtype=int)
        for r in range(5):
            row = r * 131
            for c in range(5):
                col = c * 131
                counts[r, c] = np.count_nonzero(grid[row:row+131, col:col+131] == steps)

        total = np.count_nonzero(grid == steps)
        assert counts.sum() == total  # verify the my slices covered everything

        print(counts)

        # counts = np.array([[   0,  925, 5541,  937,    0],
        #                    [ 925, 6459, 7354, 6444,  937],
        #                    [5558, 7354, 7362, 7354, 5538],
        #                    [ 936, 6461, 7354, 6456,  941],
        #                    [   0,  936, 5555,  941,    0]])
        oddFull = counts[2,2]
        evenFull = counts[1,2]
        oddEdges = counts[(1, 1, 3, 3), (1, 3, 1, 3)].sum()
        evenEdges = counts[(0, 0, 4, 4), (1, 3, 1, 3)].sum()
        corners = counts[(0, 2, 2, 4), (2, 0, 4, 2)].sum()

        # Verify that I added every square somewhere
        assert oddFull + 4 * evenFull + oddEdges + 2 * evenEdges + corners == total
        
        # XXX: Insert derevation here
        steps = 26501365
        N = steps // 131

        answer = ((N-1)*(N-1) * oddFull +
                  ( N )*( N ) * evenFull +
                  (N-1) * oddEdges +
                  ( N ) * evenEdges +
                  corners) 

        return answer
    
if __name__ == '__main__':
    problem = Day21()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



