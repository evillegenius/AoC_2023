#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np

class DayXX:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('DayXX')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        ########################################################################
        # If the puzzle is not grid/map based, delete these lines.
        gridKey = {'.': 0, '#': 1, 'O': 2}
        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.grid = np.zeros((self.height, self.width), dtype=int)
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                self.grid[row, col] = gridKey[ch]
        #
        ########################################################################


    def Part1(self):
        answer = 0
        return answer

    def Part2(self):
        answer = 0
        return answer
    
if __name__ == '__main__':
    problem = DayXX()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



