#!/usr/bin/env python
"""
Advent of Code, Day 1: Trebuchet?!
"""
# Full details at bottom

import sys
import re

class Day01:
    def __init__(self):
        self.input = None
        self.digitLookup = dict(zero='0',
                                one='1',
                                two='2',
                                three='3',
                                four='4',
                                five='5',
                                six='6',
                                seven='7',
                                eight='8',
                                nine='9')
        for i in range(10):
            self.digitLookup[str(i)] = str(i)

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day01')
        parser.add_argument('input', nargs='?', default='input.txt')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Digit(self, match):
        return self.digitLookup[match.group(1)]
    
    def Part1(self):
        total = 0
        for n, line in enumerate(self.lines):
            text = re.sub('[^\d]', '', line)
            try:
                number = int(text[0] + text[-1])
            except IndexError:
                number = -999 # So Part1 can run on example2
            #print(f'line {n:4d}: {number}: {line}')
            total += number
        return total

    def Part2(self):
        total = 0
        digitsPat = r'(\d|zero|one|two|three|four|five|six|seven|eight|nine)'
        firstPat = re.compile(r'^.*?' + digitsPat)
        lastPat = re.compile(r'^.*' + digitsPat)
        for n, line in enumerate(self.lines):
            match = firstPat.search(line)
            if not match:
                print(f'Could not find first digit on line {n}: {line}')
                continue

            first = self.Digit(match)

            match = lastPat.search(line)
            if not match:
                print(f'Could not find last digit on line {n}: {line}')
                continue

            last = self.Digit(match)

            number = int(first + last)
            #print (f'line {n:4d}: {number}: {line}')
            total += number
        return total

if __name__ == '__main__':
    problem = Day01()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



# Full problem description:
"""
--- Day 1: Trebuchet?! ---

Something is wrong with global snow production, and you've been selected to take
a look. The Elves have even given you a map; on it, they've used stars to mark
the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you
need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day
in the Advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough")
and where they're even sending you ("the sky") and why your map looks mostly
blank ("you sure ask a lot of questions") and hang on did you just say the sky
("of course, where do you think snow comes from") when you realize that the
Elves are already loading you into a trebuchet ("please hold still, we need to
strap you in").

As they're making the final adjustments, they discover that their calibration
document (your puzzle input) has been amended by a very young Elf who was
apparently just excited to show off her art skills. Consequently, the Elves are
having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line
originally contained a specific calibration value that the Elves now need to
recover. On each line, the calibration value can be found by combining the first
digit and the last digit (in that order) to form a single two-digit number.

For example:

    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and
77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the
calibration values?


Your puzzle answer was [redacted].



--- Part Two --- 

Your calculation isn't quite right. It looks like some of the
digits are actually spelled out with letters: one, two, three, four, five, six,
seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last
digit on each line. For example:

    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and
76. Adding these together produces 281.

What is the sum of all of the calibration values?


Your puzzle answer was [redacted].
"""

