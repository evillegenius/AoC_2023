#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
from collections import namedtuple

class Dir(namedtuple('Dir', 'dr dc')):
    pass

NORTH = Dir(-1, 0)
SOUTH = Dir(1, 0)
WEST = Dir(0, -1)
EAST = Dir(0, 1)

class Pos(namedtuple('Pos', 'row col')):
    def __add__(self, dir):
        return Pos(self.row + dir.dr, self.col + dir.dc)
    
class Day16:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day16')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.height = len(self.lines)
        self.width = len(self.lines[0])

    def Energize(self, pos, dir):

        seen = set()
        todo = set()
        todo.add((pos, dir))
        while todo:
            state = todo.pop()
            if state in seen:
                continue

            p, d = state

            if not (0 <= p[0] < self.height) or not (0 <= p[1] < self.width):
                continue

            seen.add(state)

            cell = self.lines[p[0]][p[1]]
            if cell == '.':
                todo.add((p + d, d))
            elif cell == '-':
                if d in (EAST, WEST):
                    todo.add((p + d, d))
                else:
                    todo.add((p + EAST, EAST))
                    todo.add((p + WEST, WEST))
            elif cell == '|':
                if d in (NORTH, SOUTH):
                    todo.add((p + d, d))
                else:
                    todo.add((p + NORTH, NORTH))
                    todo.add((p + SOUTH, SOUTH))
            elif cell == '/':
                if d == NORTH:
                    todo.add((p + EAST, EAST))
                elif d == EAST:
                    todo.add((p + NORTH, NORTH))
                elif d == SOUTH:
                    todo.add((p + WEST, WEST))
                elif d == WEST:
                    todo.add((p + SOUTH, SOUTH))
            elif cell == '\\':
                if d == NORTH:
                    todo.add((p + WEST, WEST))
                elif d == WEST:
                    todo.add((p + NORTH, NORTH))
                elif d == SOUTH:
                    todo.add((p + EAST, EAST))
                elif d == EAST:
                    todo.add((p + SOUTH, SOUTH))
            else:
                assert False, f"Unknown grid cell char {cell!r}"

        points = set(state[0] for state in seen)

        return len(points)

    def Part1(self):
        answer = self.Energize(Pos(0, 0), EAST)
        return answer

    def Part2(self):
        results = []
        for row in range(self.height):
            p1, d1 = Pos(row, 0), EAST
            results.append((self.Energize(p1, d1), p1, d1))
            p2, d2 = Pos(row, self.width - 1), WEST
            results.append((self.Energize(p2, d2), p2, d2))
        for col in range(self.width):
            p1, d1 = Pos(0, col), SOUTH
            results.append((self.Energize(p1, d1), p1, d1))
            p2, d2 = Pos(self.height - 1, col), NORTH
            results.append((self.Energize(p2, d2), p2, d2))

        best = max(results)
        print(best)          
        answer = best[0]
        return answer
    
if __name__ == '__main__':
    problem = Day16()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



