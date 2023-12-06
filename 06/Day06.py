#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import math

class Day06:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day06')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Part1(self):
        ways = []
        times = list(map(int, self.lines[0].split(':')[1].split()))
        dists = list(map(int, self.lines[1].split(':')[1].split()))
        for time, dist in zip(times, dists):
            a, b, c = 1, -time, dist
            min_time = math.floor((-b - math.sqrt(b*b - 4*c))/2 + 1)
            max_time = time - min_time
            ways.append(max_time - min_time + 1)
            print(f'time={time}, dist={dist}, ways={ways[-1]}')

        answer = math.prod(ways)
        return answer

    def Part2(self):
        answer = 0
        ways = []
        times = list(map(int, self.lines[0].split(':')[1].replace(' ', '').split()))
        dists = list(map(int, self.lines[1].split(':')[1].replace(' ', '').split()))
        for time, dist in zip(times, dists):
            a, b, c = 1, -time, dist
            min_time = math.floor((-b - math.sqrt(b*b - 4*c))/2 + 1)
            max_time = time - min_time
            ways.append(max_time - min_time + 1)
            print(f'time={time}, dist={dist}, ways={ways[-1]}')

        answer = math.prod(ways)
        return answer
    
if __name__ == '__main__':
    problem = Day06()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



