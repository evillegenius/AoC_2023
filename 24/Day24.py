#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np
from collections import namedtuple

class Pos(namedtuple('Pos', 'x y')):
    pass

class Line(namedtuple('Line', 'x y z dx dy dz')):
    def Intersect2(self, other):
        denom = self.dx * other.dy - self.dy * other.dx
        if denom != 0:
            t = ((self.y - other.y) * other.dx - (self.x - other.x) * other.dy) / denom
            u = ((self.y - other.y) * self.dx  - (self.x - other.x) * self.dy)  / denom
            return Pos(self.x + t * self.dx, self.y + t * self.dy), t, u
        else:
            return None, None, None

class Day24:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day24')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.text = input.read().strip().split('\n')

        self.lines = []
        for text in self.text:
            parts = list(map(int, text.replace('@', ' ').replace(',', ' ').split()))
            self.lines.append(Line(*parts))

        import pprint
        pprint.pprint(self.lines)


    def Part1(self):
        answer = 0
        testMin = 200_000_000_000_000
        testMax = 400_000_000_000_000
        for i in range(len(self.lines) - 1):
            for j in range(i+1, len(self.lines)):
                p, t, u = self.lines[i].Intersect2(self.lines[j])
                # print(f'{i}, {j}: p={p}, t={t}, u={u}')
                if p and t > 0 and u > 0:
                    if testMin <= p.x <= testMax and testMin <= p.y <= testMax:
                       answer += 1
        return answer

    def Part2(self):
        answer = 0
        return answer
    
if __name__ == '__main__':
    problem = Day24()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



