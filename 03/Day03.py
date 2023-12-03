#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re


class Day03:
    def __init__(self):
        self.input = None

        self.lines = []

        self.stars = {}

        # Map from star '*' symbols to the list of part numbers that are
        # adjacent to them.
        self.symbolPat = re.compile(r'[^.\d]')

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day03')
        parser.add_argument('input', nargs='?', default='input.txt')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def FoundSymbol(self, row, start, end):
        """Return True if a symbol was found adjacent to this part number"""
        clampedStart = max(0, start-1)
        for r in (row-1, row, row+1):
            if 0 <= r < len(self.lines):
                if self.symbolPat.search(self.lines[r][clampedStart:end+1]):
                    return True
                
        return False


    def Part1(self):
        """Scan the map for part numbers and sum them"""
        answer = 0
        for i, line in enumerate(self.lines):
            for match in re.finditer('\d+', line):
                partNum = int(match[0])
                start, end = match.start(), match.end()
                if self.FoundSymbol(i, start, end):
                    answer += partNum
        return answer


    def FindStars(self, row, start, end, partNum):
        """Find '*' symbols adjacent to the partNum and populate self.stars with them."""
        clampedStart = max(0, start-1)
        for r in (row-1, row, row+1):
            if 0 <= r < len(self.lines):
                starCol = self.lines[r].find('*', clampedStart, end+1)
                if starCol != -1:
                    self.stars.setdefault((r, starCol), []).append(partNum)


    def Part2(self):
        """
        Scan for gears ('*' symbols) adjacent to 2 partNums, multiply the 2 partNums
        and return the sum of the results.
        """
        answer = 0
        for i, line in enumerate(self.lines):
            for match in re.finditer('\d+', line):
                partNum = int(match[0])
                start, end = match.start(), match.end()
                self.FindStars(i, start, end, partNum)

        for starPos, partNums in self.stars.items():
            if len(partNums) == 2:
                answer += partNums[0] * partNums[1]

        return answer


if __name__ == '__main__':
    problem = Day03()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')


"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

Your puzzle answer was 519444.


--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

Your puzzle answer was 74528807.
"""
