#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import itertools
import re

def Alternate(seq1, seq2):
    a = iter(seq1)
    b = iter(seq2)
    try:
        while True:
            yield next(a)
            yield next(b)
    except StopIteration:
        return


class Day12:
    def __init__(self):
        self.input = None

        self.lines = []

        self.patterns = [
            re.compile(rf'^[. ?][#?]{{{n}}}[. ?]?$')
            for n in range(20)
        ]
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day12')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.grids = [line.split()[0]
                       for line in self.lines]
        self.counts = [list(map(int, line.split()[1].split(',')))
                       for line in self.lines]

        
    def CountMatches(self, grid, counts):
        # Pad grid to aid with matching
        grid = ' ' + grid + ' '
        print(f'{grid}  {counts}')
        # offset to the next group (or end)
        deltas = [count + 1 for count in counts]
        start = 1
        starts = []
        # Counts, deltas, and starts all have the same length
        indices = tuple(range(len(counts)))
        for i in indices:
            starts.append(start)
            start += deltas[i]

        matches = 0
        while True:
            update = -1
            prev = 0
            for i in indices:
                if (self.patterns[counts[i]].match(grid[starts[i]-1:starts[i] + deltas[i]]) and
                    '#' not in grid[prev:starts[i]]):
                    # this one could work, see if we skipped over a #
                    prev = starts[i] + counts[i]
                    continue # to the next index
                else:
                    update = i
                    break
            else:
                update = len(counts) - 1
                matches += 1

                # XXX debugging
                result = ''
                for i in indices:
                    result += '.' * (starts[i] - len(result))
                    result += '#' * (counts[i])
                result += '.' * (len(grid) - len(result))
                print(f' {result[1:-1]}   {starts}')
                # XXX end debugging

            while update >= 0:
                starts[update] += 1
                for i in indices[update+1:]:
                    starts[i] = starts[i-1] + deltas[i-1]

                if starts[-1] + deltas[-1] > len(grid):
                    update -= 1
                    continue
                else:
                    break
            else:
                break

        print(f'  -> {matches}\n')
        return matches




            





    def Part1(self):
        answer = 0
        for grid, counts in zip(self.grids, self.counts):
            answer += self.CountMatches(grid, counts)
        return answer

    def Part2(self):
        answer = 0

        return answer
    
if __name__ == '__main__':
    problem = Day12()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



