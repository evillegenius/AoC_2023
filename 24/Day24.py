#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np
from collections import namedtuple

Point2 = namedtuple('Point2', 'x y')
Point3 = namedtuple('Point3', 'x y z')

Vector3 = namedtuple('Vector3', 'dx dy dz')

class Line(namedtuple('Line', 'x y z dx dy dz')):
    def Intersect2(self, other):
        denom = self.dx * other.dy - self.dy * other.dx
        if denom != 0:
            t = ((self.y - other.y) * other.dx - (self.x - other.x) * other.dy) / denom
            u = ((self.y - other.y) * self.dx  - (self.x - other.x) * self.dy)  / denom
            return Point2(self.x + t * self.dx, self.y + t * self.dy), t, u
        else:
            return None, None, None
        
    def P(self):
        return Point3(*self[:3])
    
    def V(self):
        return Vector3(*self[3:])


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

        # I think secret is to take hailstones in pairs. Here's how.
        # We're solving for rockLine = Line(x, y, z, dx, dy, dz)
        # where the 6 unknowns are x, y, z, dx, dy, dz.
        # 
        # So the position of the rock at time t is:
        #     x + t * dx, y + t * dy, z + t * dz
        # And the position of hailstone[i] at time t is:
        #     hx[i] + t * hdx[i], hy[i] + t * hdy[1], hz[i] + t * hdz[i]
        #
        # In order to intersect, they must have the same value at some time t.
        #     x + t * dx = hx[i] + t * hdx[i], ...
        #     t = (hx[i] - x) / (dx - hdx[i])
        #       = (hy[i] - y) / (dy - hdy[i])
        #       = (hz[i] - z) / (dz - hdz[i])
        #
        # Ignoring z for a moment, we get:
        #     (hx[i] - x) * (dy - hdy[i]) = (hy[i] - y) * (dx - hdx[i])
        #     hx[i]*dy - hx[i]*hdy[i] - x*dy + hdy[i]*x = hy[i]*dx - hy[i]*hdx[i] - y*dx + hdx[i]*y
        #
        # Instantiating this equation for i = 0 and 1 gives us:
        #     hx[0]*dy - hx[0]*hdy[0] - x*dy + hdy[0]*x =  hy[0]*dx - hy[0]*hdx[0] - y*dx + hdx[0]*y
        #     hx[1]*dy - hx[1]*hdy[1] - x*dy + hdy[1]*x =  hy[1]*dx - hy[1]*hdx[1] - y*dx + hdx[1]*y
        #
        # Negating and adding (simpler for me to get right than subtracting...)
        #     hx[0]*dy - hx[0]*hdy[0] - x*dy + hdy[0]*x =  hy[0]*dx - hy[0]*hdx[0] - y*dx + hdx[0]*y
        #    -hx[1]*dy + hx[1]*hdy[1] + x*dy - hdy[1]*x = -hy[1]*dx + hy[1]*hdx[1] + y*dx - hdx[1]*y
        #   ========================================================================================
        #     (hx[0] - hx[1])*dy - hx[0]*hdy[0] + hx[1]*hdy[1] + (hdy[0] - hdy[1])*x =
        #     (hy[0] - hy[1])*dx - hy[0]*hdx[0] + hy[1]*hdx[1] + (hdx[0] - hdx[1])*y
        #
        # Rearranging gives us:
        #     (hdy[0] - hdy[1])*x + (hdx[1] - hdx[0])*y + (hy[1] - hy[0])*dx + (hx[0] - hx[1])*dy =
        #         hx[0]*hdy[0] - hx[1]*hdy[1] - hy[0]*hdx[0] + hy[1]*hdx[1]
        # or:
        #     a * x + b * y + c * dx + d * dy = k
        # where:
        #     a = hdy[0] - hdy[1]
        #     b = hdx[1] - hdx[0]
        #     c = hy[1] - hy[0]
        #     d = hx[0] - hx[1]
        #     k = hx[0]*hdy[0] - hx[1]*hdy[1] - hy[0]*hdx[0] + hy[1]*hdx[1]
        #
        # This needs to be repeated substituting z for y everywhere to get the final 2 missing 
        # values. But this is a form I can ask numpy to solve!

        # There are 4 unknowns (at a time) so we need 4 rows for our matrix, that means
        # operating on 8 hailstones. I'm assuming that if I hit the first 4 then I will
        # hit all the rest.

        aY = np.zeros((4, 4), dtype=float)
        aZ = np.zeros((4, 4), dtype=float)
        kY = np.zeros((4,1), dtype=float)
        kZ = np.zeros((4,1), dtype=float)
        for i in range(4):
            aY[i] = self.Coeff(self.lines[i], self.lines[i+1], 0, 1, 3, 4)
            aZ[i] = self.Coeff(self.lines[i], self.lines[i+1], 0, 2, 3, 5)
            kY[i] = self.Const(self.lines[i], self.lines[i+1], 0, 1, 3, 4)
            kZ[i] = self.Const(self.lines[i], self.lines[i+1], 0, 2, 3, 5)

        solveY = np.linalg.solve(aY, kY)
        solveZ = np.linalg.solve(aZ, kZ)

        assert abs(solveY[0] - solveZ[0]) < 0.5
        assert abs(solveY[2] - solveZ[2]) < 0.5
        print(f'Rock: {(solveY[0,0], solveY[1,0], solveZ[1,0])} @ {(solveY[2,0], solveY[3,0], solveZ[3,0])}')
        return round(solveY[0,0] + solveY[1,0] + solveZ[1,0])


    def Coeff(self, l0, l1, x, y, dx, dy):
        return (l0[dy] - l1[dy],
                l1[dx] - l0[dx],
                l1[y] - l0[y],
                l0[x] - l1[x])
    
    def Const(self, l0, l1, x, y, dx, dy):
        return l0[x]*l0[dy] - l1[x]*l1[dy] - l0[y]*l0[dx] + l1[y]*l1[dx]
    
if __name__ == '__main__':
    problem = Day24()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



