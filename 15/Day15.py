#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re

class Day15:
    def __init__(self):
        self.input = None

        self.steps = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day15')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.steps = input.read().strip().split(',')

    def Hash(self, step):
        result = 0
        for ch in step:
            result += ord(ch)
            result *= 17
            result %= 256

        return result

    def Part1(self):
        answer = 0
        for step in self.steps:
            answer += self.Hash(step)
        return answer

    def Part2(self):
        answer = 0
        hashmap = {}
        stepPat = re.compile(r'^([^=-]+)([=-])(\d+)?$')
        for step in self.steps:
            match = stepPat.match(step)
            assert match, f'Fatal: {step!r} failed to match!'

            label, op, lens = match.groups()

            box = self.Hash(label)
            hashmap.setdefault(box, {})
            if op == '=':
                hashmap[box][label] = int(lens)
            else:
                hashmap[box].pop(label, None)

        for box in hashmap:
            for slot, lens in enumerate(hashmap[box].values()):
                power = (box + 1) * (slot + 1) * lens
                answer += power

        return answer
    
if __name__ == '__main__':
    problem = Day15()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



