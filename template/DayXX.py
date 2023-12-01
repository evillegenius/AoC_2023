#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys

class DayXX:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('DayXX')
        parser.add_argument('input', nargs='?', default='input.txt')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Part1(self):
        return 0

    def Part2(self):
        return 0
    
if __name__ == '__main__':
    problem = DayXX()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



