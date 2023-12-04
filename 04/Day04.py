#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys

class Day04:
    def __init__(self):
        self.input = None

        self.matchCount = []

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day04')
        parser.add_argument('input', nargs='?', default='input.txt')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Part1(self):
        answer = 0
        for line in self.lines:
            game, rest = line.split(':')
            winners, numbers = rest.split('|')

            winners = set(map(int, winners.split()))
            numbers = set(map(int, numbers.split()))

            matches = len(winners & numbers)
            self.matchCount.append(matches)
            if matches:
                points = 2 ** (matches - 1)
                answer += points
        return answer

    def Part2(self):
        answer = 0
        counts = [1] * len(self.matchCount)
        for i, n in enumerate(self.matchCount):
            for j in range(i+1, i+n+1):
                counts[j] += counts[i]

        answer = sum(counts)
        return answer
    
if __name__ == '__main__':
    problem = Day04()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



