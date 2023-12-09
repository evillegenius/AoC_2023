#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys

class Day09:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day09')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        for i, line in enumerate(self.lines):
            self.lines[i] = list(map(int, line.split()))


    def Extrapolate(self, line):
        deltas = [line]
        while any(deltas[-1]):
            deltas.append([deltas[-1][i] - deltas[-1][i-1] for i in range(1, len(deltas[-1]))])

        last = 0
        for i in range(len(deltas) - 1, -1, -1):
            last = deltas[i][-1] + last

        return last

    def Part1(self):
        answer = 0
        for line in self.lines:
            answer += self.Extrapolate(line)
        return answer

    def ExtrapolateBack(self, line):
        deltas = [line]
        while any(deltas[-1]):
            deltas.append([deltas[-1][i] - deltas[-1][i-1] for i in range(1, len(deltas[-1]))])

        first = 0
        for i in range(len(deltas) - 1, -1, -1):
            first = deltas[i][0] - first

        return first

    def Part2(self):
        answer = 0
        for line in self.lines:
            answer += self.ExtrapolateBack(line)
        return answer
    
if __name__ == '__main__':
    problem = Day09()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



