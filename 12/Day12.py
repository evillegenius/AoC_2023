#!/usr/bin/env python3
"""
Advent of Code 2023, Day 12
"""
import re
import functools

class Day12:
    def __init__(self):
        self.input = None

        self.lines = []

        self.patterns = [
            re.compile(rf'(^|(?<=[^#]))'  # preceded by beginning or not '#'
                       rf'([#?]{{{n}}})'  # exactly n '#' or '?'
                       rf'((?=[^#])|$)')  # followed by not '#' or end
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
        self.counts = [tuple(map(int, line.split()[1].split(',')))
                       for line in self.lines]

    # functools.cache for the win! It creates a decorated version of the method that
    # memoizes its input and outputs. If the same input arguments are provided again
    # it simply returns them. This is *huge* for a recursive method since it also
    # short circuits all the recursive calls.
    @functools.cache
    def CountMatches(self, grid, counts):
        matchCount = 0

        if not counts and '#' not in grid:
            # Empty counts matches a string without #
            return 1
        elif not grid or not counts:
            return 0

        count = counts[0]

        # Cannot start a match if there's less than this much space in grid
        lastStart = len(grid) - sum(counts) - len(counts[1:])
        lastEnd = lastStart + count

        searchStart = 0
        while searchStart <= lastStart:
            # There appears to be a bug in the start, end parameters of re.search
            # when combined with look behind and look ahead assertions. A look
            # behind assertion like (?<=[^#]) will happily look at the string
            # contents before the start value, but a look ahead assertion like
            # (?=^[#]) will not look after the end parameter. Instead it appears
            # to treat the end parameter as if it were really the end of the
            # string.
            # 
            # To work around this, I'm using lastEnd+1 so the search always
            # includes the character one past the last possible ending point
            # of the current group so there's something to match that look
            # ahead assertion against.
            match = self.patterns[count].search(grid, searchStart, lastEnd + 1)
            if match:
                foundStart = match.start(2) # where the group started

                # If we're searching after a '#' then the match is invalid.
                if '#' in grid[:foundStart]:
                    break

                # Recurse
                matchCount += self.CountMatches(grid[foundStart + count + 1:], counts[1:])

                # Start the next search one past the start of this search.
                searchStart = foundStart + 1
            else:
                # We did not find any (more) matches for this group. We're done.
                break

        # print(f'{grid} {",".join(map(str, counts))} -> {matchCount}')
        return matchCount


    def Part1(self):
        answer = 0
        for grid, counts in zip(self.grids, self.counts):
            answer += self.CountMatches(grid, counts)
            self.CountMatches.cache_clear()
        return answer


    def Part2(self):
        answer = 0
        for grid, counts in zip(self.grids, self.counts):
            grid = '?'.join([grid]*5)
            counts = counts * 5
            # print('='*80)
            result = self.CountMatches(grid, counts)
            # print(f'{grid}  {counts} -> {result}')
            answer += result
            # Reset the memoization cache
            self.CountMatches.cache_clear()
        return answer


if __name__ == '__main__':
    problem = Day12()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



