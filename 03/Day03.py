#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re


class Day03:
    def __init__(self):
        self.input = None

        self.lines = []

        self.stars = {}

        self.symbolPat = re.compile(r'[^.\d]')

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day03')
        parser.add_argument('input', nargs='?', default='input.txt')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def FoundSymbol(self, row, start, end):
        clampedStart = max(0, start-1)
        for r in (row-1, row, row+1):
            if 0 <= r < len(self.lines):
                if self.symbolPat.search(self.lines[r][clampedStart:end+1]):
                    return True
                
        return False


    def Part1(self):
        answer = 0
        for i, line in enumerate(self.lines):
            for match in re.finditer('\d+', line):
                partNum = int(match[0])
                start, end = match.start(), match.end()
                if self.FoundSymbol(i, start, end):
                    answer += partNum
        return answer


    def FindStars(self, row, start, end, partNum):
        clampedStart = max(0, start-1)
        for r in (row-1, row, row+1):
            if 0 <= r < len(self.lines):
                starCol = self.lines[r].find('*', clampedStart, end+1)
                if starCol != -1:
                    self.stars.setdefault((r, starCol), []).append(partNum)


    def Part2(self):
        answer = 0
        for i, line in enumerate(self.lines):
            for match in re.finditer('\d+', line):
                partNum = int(match[0])
                start, end = match.start(), match.end()
                self.FindStars(i, start, end, partNum)

        for starPos, partNums in self.stars.items():
            if len(partNums) == 2:
                answer += partNums[0] * partNums[1]

        return answer


if __name__ == '__main__':
    problem = Day03()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



