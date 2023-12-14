#!/usr/bin/env python3
"""
Advent of Code Day 14.

This is not actually a complete solution. For part 2 we're supposed to
iterate 1 billion times. This only iterates 1000. That was enough to
determine that there was a repeating pattern of length 42 cycles in my
particular input data. 1 billion cycles is iteration 999999999 (since
we start with 0 instead of 1) and 999999999 % 42 == 33. So find an
iteration like 957 because 957 % 42 == 33 and report it's value.
"""
import sys
import numpy as np

NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4

EMPTY = 0
SQUARE = 1
ROUND = 2

class Day14:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day14')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.grid = np.zeros((len(self.lines), len(self.lines[0])), dtype=int)
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                self.grid[row,col] = '.#O'.index(ch)

        # print(self.grid)


    def TiltNorth(self, grid):
        rocks = np.argwhere(grid == ROUND)

        for rock in rocks:
            row, col = rock
            while row > 0 and grid[row-1, col] == 0:
                grid[row-1, col] = ROUND
                grid[row, col] = EMPTY
                row -= 1
        return grid

    def Cycle(self, grid):
        self.TiltNorth(grid)
        score = self.Score(grid)
        # print(f' North: {score} '.center(40, '-'))
        # print(grid)
        self.TiltNorth(np.rot90(grid, k=3))
        score = self.Score(grid)
        # print(f' West: {score} '.center(40, '-'))
        # print(grid)
        self.TiltNorth(np.rot90(grid, k=2))
        score = self.Score(grid)
        # print(f' South: {score} '.center(40, '-'))
        # print(grid)
        self.TiltNorth(np.rot90(grid, k=1))
        score = self.Score(grid)
        # print(f' East: {score} '.center(40, '-'))
        # print(grid)

    def Score(self, grid):
        rocks = np.where(grid == ROUND)[0]
        rows = grid.shape[0]
        score = np.sum(rows - rocks)
        return score

    def Cycles(self, grid, count):
        for i in range(count):
            self.Cycle(grid)
            self.scores.append(self.Score(grid))
            print(f'Cycle {i}: {self.scores[i]} ')


    def Part1(self):
        answer = 0

        grid = self.grid.copy()
        # self.TiltNorth(grid)

        # rocks = np.argwhere(grid == ROUND)

        # rows = grid.shape[0]

        # rocks = rows - rocks

        # answer = np.sum(rocks[:,0])

        answer = self.Score(grid)

        return answer

    def Part2(self):
        answer = 0
        self.scores = []
        self.Cycles(self.grid.copy(), 1000)
        return answer
    
if __name__ == '__main__':
    problem = Day14()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



