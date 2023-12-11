#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
from collections import namedtuple
import numpy as np

class Pos(namedtuple('Pos', 'row col')):
    def Dist(self, other):
        return abs(self.row - other.row) + abs(self.col - other.col)


class Day11:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day11')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.width = len(self.lines[0])
        self.height = len(self.lines)


    def Part1(self):
        answer = 0
        sky = np.zeros((self.height, self.width), dtype=int)

        id = 0
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                if ch != '.':
                    id += 1
                    sky[row,col] = id

        for row in reversed(range(sky.shape[0])):
            if not any(sky[row,:]):
                sky = np.insert(sky, row, 0, axis=0)

        for col in reversed(range(sky.shape[1])):
            if not any(sky[:,col]):
                sky = np.insert(sky, col, 0, axis=1)

        positions = np.argwhere(sky)
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                dist = (abs(positions[i][0] - positions[j][0]) +
                        abs(positions[i][1] - positions[j][1]))
                answer += dist

        return answer

    def Part2(self):
        answer = 0
        factor = 1_000_000
        sky = np.zeros((self.height, self.width), dtype=int)

        id = 0
        positions = []
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                if ch != '.':
                    id += 1
                    sky[row,col] = id
                    positions.append(Pos(row, col))

        emptyRows = []
        for row in range(sky.shape[0]):
            if not any(sky[row,:]):
                emptyRows.append(row)

        emptyCols = []
        for col in range(sky.shape[1]):
            if not any(sky[:,col]):
                emptyCols.append(col)

        answer = 0
        for i, pos in enumerate(positions):
            row, col = pos
            for j, emptyRow in enumerate(emptyRows):
                if emptyRow > row:
                    row += (factor - 1) * j
                    break
            else:
                row += (factor - 1) * len(emptyRows)

            for j, emptyCol in enumerate(emptyCols):
                if emptyCol > col:
                    col += (factor - 1) * j
                    break
            else:
                col += (factor - 1) * len(emptyCols)

            positions[i] = Pos(row, col)

        for i, iPos in enumerate(positions):
            for j, jPos in enumerate(positions[i+1:]):
                dist = iPos.Dist(jPos)
                answer += dist

        return answer
    
if __name__ == '__main__':
    problem = Day11()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



