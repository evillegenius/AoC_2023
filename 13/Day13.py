#!/usr/bin/env python
"""
<Problem description here>
"""
import sys
import numpy as np

class Day13:
    def __init__(self):
        self.input = None

        self.lines = []
        self.maps = []

        # Answers we found in part 1 so we don't find them again in part 2
        self.rows = []
        self.cols = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day13')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def MakeMap(self, lines):
        m = np.zeros((len(lines), len(lines[0])), dtype=int)
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                m[r, c] = (ch == '#')
        return m
    

    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.maps = []
        start = 0
        for i, line in enumerate(self.lines):
            if not line:
                self.maps.append(self.MakeMap(self.lines[start:i]))
                start = i + 1
        else:
            self.maps.append(self.MakeMap(self.lines[start:]))


    def FindRow(self, map):
        self.rows.append(-1)
        for r in range(map.shape[0]-1):
            if np.array_equal(map[r], map[r+1]):
                a, b = r, r+1
                while 0 <= a and b < map.shape[0] and np.array_equal(map[a], map[b]):
                    a -= 1
                    b += 1
                else:
                    if a < 0 or b >= map.shape[0]:
                        # we matched all the way to the edge
                        self.rows[-1] = r
                        return 100 * (r + 1)
                    
        return 0
    

    def FindCol(self, map):
        self.cols.append(-1)
        for c in range(map.shape[1]-1):
            if np.array_equal(map[:,c], map[:,c+1]):
                a, b = c, c+1
                while 0 <= a and b < map.shape[1] and np.array_equal(map[:,a], map[:,b]):
                    a -= 1
                    b += 1
                else:
                    if a < 0 or b >= map.shape[1]:
                        # we matched all the way to the edge
                        self.cols[-1] = c
                        return (c + 1)
                    
        return 0


    def Part1(self):
        answer = 0
        for map in self.maps:
            answer += self.FindRow(map) + self.FindCol(map)
        return answer

    def FindNearRow(self, map, avoid):
        for r in range(map.shape[0]-1):
            if r == avoid:
                continue
            delta = np.count_nonzero(map[r] != map[r+1])

            if delta <= 1:
                a, b = r-1, r+2
                while 0 <= a and b < map.shape[0] and delta <= 1:
                    delta += np.count_nonzero(map[a] != map[b])
                    a -= 1
                    b += 1
                else:
                    if delta == 1:
                        # we matched all the way to the edge
                        return 100 * (r + 1)
                    
        return 0
    

    def FindNearCol(self, map, avoid):
        for c in range(map.shape[1]-1):
            if c == avoid:
                continue
            delta = np.count_nonzero(map[:,c] != map[:,c+1])

            if delta <= 1:
                a, b = c-1, c+2
                while 0 <= a and b < map.shape[1] and delta <= 1:
                    delta += np.count_nonzero(map[:,a] != map[:,b])
                    a -= 1
                    b += 1
                else:
                    if delta == 1:
                        # we matched all the way to the edge
                        return (c + 1)
                    
        return 0

    def Part2(self):
        answer = 0
        for i, map in enumerate(self.maps):
            n = self.FindNearRow(map, self.rows[i]) + self.FindNearCol(map, self.cols[i])
            assert n, f"Map {i} failed Part 2 test\n{map}"
            answer += n
        return answer
    
if __name__ == '__main__':
    problem = Day13()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



