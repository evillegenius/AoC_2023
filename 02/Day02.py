#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re

class Day02:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day02')
        parser.add_argument('input', nargs='?', default='input.txt')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Part1(self):
        total = 0
        for line in self.lines:
            game, cubeSets = line.split(':')
            game = int(game[5:])
            
            possible = True
            cubeSets = cubeSets.split(';')
            for cubeSet in cubeSets:
                colorCounts = dict(red=0, green=0, blue=0)
                colorCubes = cubeSet.split(',')
                for colorCube in colorCubes:
                    n, color = colorCube.split()
                    n = int(n)

                    colorCounts[color] = n
                if possible:
                    possible = (colorCounts['red'] <= 12 and
                                colorCounts['green'] <= 13 and
                                colorCounts['blue'] <= 14)
            if possible:
                total += game
            
        return total

    def Part2(self):
        total = 0
        for line in self.lines:
            game, cubeSets = line.split(':')
            game = int(game[5:])
            colorCounts = dict(red=0, green=0, blue=0)
            
            cubeSets = cubeSets.split(';')
            for cubeSet in cubeSets:
                colorCubes = cubeSet.split(',')
                for colorCube in colorCubes:
                    n, color = colorCube.split()
                    n = int(n)

                    colorCounts[color] = max(colorCounts[color], n)

            power = colorCounts['red'] * colorCounts['green'] * colorCounts['blue']

            total += power
        return total
    
if __name__ == '__main__':
    problem = Day02()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



