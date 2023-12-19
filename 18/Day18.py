#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import numpy as np
from collections import namedtuple

class Dir(namedtuple('Dir', 'dr dc')):
    def __mul__(self, scale):
        return Dir(self.dr * scale, self.dc * scale)
    
    # Use matrix multiply operater (@) for cross product
    def __matmul__(self, rhs):
        return self.dr * rhs.dc - self.dc * rhs.dr
    
    def __imatmul__(self, rhs):
        return self @ rhs

UP = Dir(-1, 0)
DOWN = Dir(1, 0)
LEFT = Dir(0, -1)
RIGHT = Dir(0, 1)    
    
class Pos(namedtuple('Pos', 'row col')):
    def __add__(self, delta):
        return Pos(self.row + delta.dr, self.col + delta.dc)
    
    def __iadd__(self, delta):
        # if not isinstance(delta, Dir):
        #     raise TypeError(f"unsupported operand types for +=: 'Pos' and {type(delta).__name__}")
        return self + delta
    
    def __sub__(self, other):
        if isinstance(other, Pos):
            return Dir(self.row - other.row, self.col - other.col)
        elif isinstance(other, Dir):
            return Pos(self.row - other.dr, self.col - other.dc)
        
    def __isub__(self, delta):
        # if not isinstance(delta, Dir):
        #     raise TypeError(f"unsupported operand types for -=: 'Pos' and {type(delta).__name__}")
        return self - delta

    # Use matrix multiply operater (@) for cross product
    # Taking the cross product of points is cheating, but we'll assume
    # the point is a vector from the origin
    def __matmul__(self, rhs):
        return self.row * rhs.col - self.col * rhs.row
    
    def __imatmul__(self, rhs):
        return self @ rhs
    
    
class Bounds:
    def __init__(self, pos=None):
        if pos is None:
            self.minrow = self.mincol = self.maxrow = self.maxcol = None
        else:
            self.minrow = self.maxrow = pos.row
            self.mincol = self.maxcol = pos.col

    def __iadd__(self, pos):
        self.minrow = pos.row if self.minrow is None else min(self.minrow, pos.row)
        self.mincol = pos.col if self.mincol is None else min(self.mincol, pos.col)
        self.maxrow = pos.row if self.maxrow is None else max(self.maxrow, pos.row)
        self.maxcol = pos.col if self.maxcol is None else max(self.maxcol, pos.col)

        return self

    def __repr__(self):
        return f'Bounds(minrow={self.minrow}, mincol={self.mincol}, maxrow={self.maxrow}, maxcol={self.maxcol})'
    
    def width(self):
        if self.mincol is None:
            return None
        else:
            return self.maxcol - self.mincol + 1
    
    def height(self):
        if self.minrow is None:
            return None
        else:
            return self.maxrow - self.minrow + 1
        
    def min(self):
        return Pos(self.minrow, self.mincol)
    
    def max(self):
        return Pos(self.maxrow, self.maxcol)


class Day18:

    Dirs = {'U': Dir(-1, 0),
            'D': Dir(1, 0),
            'L': Dir(0, -1),
            'R': Dir(0, 1),
            '0': Dir(0, 1),
            '1': Dir(1, 0),
            '2': Dir(0, -1),
            '3': Dir(-1, 0),
            }

    Flags = {'U': 1,
             'D': 2,
             'L': 4,
             'R': 8,
             'F': 16,
             'Vertical': 3}

    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day18')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def GetDir(self, line, part=1):
            dir, count, color = line.split()
            if part == 1:
                count = int(count)
                return self.Dirs[dir], count, self.Flags[dir]
            else:
                count = int(color[2:7], 16)
                return self.Dirs[color[7]], count, None
    

    def GetBounds(self, pos):
        bounds = Bounds(pos)
        
        for line in self.lines:
            dir, count, _ = self.GetDir(line)
            pos = pos + dir * count
            bounds += pos

        return bounds


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Part1(self):
        answer = 0

        pos = Pos(0, 0)
        bounds = self.GetBounds(pos)

        # Offset the minimum to be 0, 0
        offset = pos - bounds.min()
        pos += offset

        print(bounds)
        print(pos)
        grid = np.zeros((bounds.height(), bounds.width()), dtype=int)

        for line in self.lines:
            dir, count, flag = self.GetDir(line)
            grid[pos] |= flag
            while count > 0:
                count -= 1
                pos += dir
                grid[pos] |= flag

        print(grid)
        print(np.count_nonzero(grid))

        vertical = self.Flags['U'] | self.Flags['D']
        horizontal = self.Flags['L'] | self.Flags['R']
        fill = self.Flags['F']
        for row in range(grid.shape[0]):
            inside = False
            halfWay = 0
            for col in range(grid.shape[1]):
                cell = grid[row, col]
                v = cell & vertical
                h = cell & horizontal
                if v and not h:
                    halfWay = 0
                    inside = not inside
                elif v and h:
                    if halfWay == v:
                        halfWay = 0
                        inside = not inside
                    elif halfWay:
                        halfWay = 0
                        # Inside is unchanged
                    else:
                        # We're halfway inside
                        halfWay = v

                if inside and cell == 0:
                    grid[row, col] = fill
            else:
                assert not inside, f"Error still inside at edge of row {row}"

        answer = np.count_nonzero(grid)
        return answer


    def GetPoints(self, pos, part=1):
        # It appears that the loop is drawn in a clockwise direction
        # so we can take the "left-hand" edge of the line as the outside.
        # Assume that position x, y refers to the square meter centered
        # about (x + 0.5, y + 0.5) and then compute the exact vertex coordinate
        # appropriately.
        prevDir = Dir(-1, 0) # up
        prevPos = pos
        points = []
        
        for line in self.lines:
            dir, count, _ = self.GetDir(line, part)
            pos = pos + dir * count
            if prevDir == UP:
                if dir == RIGHT:
                    pass # prevPos is unchanged
                else:
                    prevPos += DOWN
            elif prevDir == RIGHT:
                if dir == UP:
                    pass # prevPos is unchanged
                else:
                    prevPos += RIGHT
            elif prevDir == DOWN:
                if dir == RIGHT:
                    prevPos += RIGHT
                else:
                    prevPos += Dir(1, 1)
            elif prevDir == LEFT:
                if dir == UP:
                    prevPos += DOWN
                else:
                    prevPos += Dir(1, 1)
            points.append(prevPos)

            prevPos, prevDir = pos, dir

        points.append(points[0])

        return points

    def Part2(self):
        answer = 0

        pos = Pos(0, 0)
        points = self.GetPoints(pos, part=2)

        for p in points:
            print(f'({p.row}, {p.col})')

        area = 0
        for i in range(len(points)-1):
            area += points[i] @ points[i + 1]

        print(area)
        print(area // 2)
        return answer
    
if __name__ == '__main__':
    problem = Day18()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



