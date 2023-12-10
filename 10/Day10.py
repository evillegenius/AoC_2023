#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import collections

class Pos(collections.namedtuple('Pos', 'row col')):
    def __add__(self, other):
        return Pos(self[0] + other[0], self[1] + other[1])
    
NORTH = Pos(-1,  0)
SOUTH = Pos( 1,  0)
EAST  = Pos( 0,  1)
WEST  = Pos( 0, -1)
    
class DayXX:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('DayXX')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Move(self, pos, dir):
        """Move from pos in direction dir, return new pos and dir"""
        pos = pos + dir
        mapChar = self.lines[pos[0]][pos[1]]

        newDir = None
        if mapChar in '|-':
            newDir = dir
        elif mapChar == 'L' and dir in (SOUTH, WEST):
            newDir = NORTH if dir == WEST else EAST
        elif mapChar == 'J' and dir in (SOUTH, EAST):
            newDir = NORTH if dir == EAST else WEST
        elif mapChar == '7' and dir in (EAST, NORTH):
            newDir = WEST if dir == NORTH else SOUTH
        elif mapChar == 'F' and dir in (WEST, NORTH):
            newDir = EAST if dir == NORTH else SOUTH
        else:
            assert False, f"Failed to set a new direction for pos={pos}, dir={dir}, mapChar={mapChar!r}"

        return pos, newDir


    def Part1(self):
        width = len(self.lines[0])
        height = len(self.lines)

        self.counts = [[-1] * width for _ in range(height)]

        for i, line in enumerate(self.lines):
            if 'S' in line:
                start = self.start = Pos(i, line.index('S'))
                break
        else:
            sys.exit('Failed to find start!')

        row, col = start
        dirs = []
        if row > 0 and self.lines[row-1][col] in "|7F":
            dirs.append(NORTH)
        if row < height - 1 and self.lines[row+1][col] in "|JL":
            dirs.append(SOUTH)
        if col > 0 and self.lines[row][col-1] in "-LF":
            dirs.append(WEST)
        if col < width - 1 and self.lines[row][col+1] in "-J7":
            dirs.append(EAST)
        
        assert len(dirs) == 2, f"Did not find 2 directions from {start}"
        aPos = bPos = start
        aDir, bDir = dirs

        if dirs == [NORTH, SOUTH]:
            self.startChar = '|'
        elif dirs == [NORTH, WEST]:
            self.startChar = 'J'
        elif dirs == [NORTH, EAST]:
            self.startChar = 'L'
        elif dirs == [SOUTH, WEST]:
            self.startChar = '7'
        elif dirs == [SOUTH, EAST]:
            self.startChar = 'F'
        elif dirs == [WEST, EAST]:
            self.startChar = '-'
        else:
            assert False, "Unable to determine startChar"

        self.counts[start[0]][start[1]] = 0
        step = 0
        # print(f'start = {start}')

        while True:
            aPos, aDir = self.Move(aPos, aDir)
            # print(f'aPos = {aPos}, aDir = {aDir}')
            bPos, bDir = self.Move(bPos, bDir)
            # print(f'bPos = {bPos}, bDir = {bDir}')
            step += 1

            assert self.counts[aPos[0]][aPos[1]] == -1, "cycle at aPos={apos}"
            self.counts[aPos[0]][aPos[1]] = step

            assert self.counts[bPos[0]][bPos[1]] in (-1, step), "cycle at bPos={apos}"
            self.counts[bPos[0]][bPos[1]] = step

            if aPos == bPos:
                break

        return step

    def Part2(self):
        """Count the squares inside the loop. They are squares where count == -1
        and the number of squares we've crossed that are not -1 is odd. The tricky
        bit is that something like 'F-7' is not a crossing but 'F-J' is.s"""
        answer = 0
        crossingChars = ''
        self.lines[self.start[0]] = self.lines[self.start[0]].replace('S', self.startChar)
        for row, rowCounts in enumerate(self.counts):
            crossings = 0
            for col, count in enumerate(rowCounts):
                if count == -1:
                    answer += crossings % 2
                else:
                    mapChar = self.lines[row][col]
                    if crossingChars:
                        if mapChar in crossingChars:
                            crossings += 1
                            crossingChars = ''
                        elif mapChar in nonCrossingChars:
                            crossingChars = ''
                        elif mapChar == '-':
                            continue
                    else:
                        if mapChar in 'LJ':
                            crossingChars = '7F'
                            nonCrossingChars = 'LJ'
                        elif mapChar in '7F':
                            crossingChars = 'LJ'
                            nonCrossingChars = '7F'
                        elif mapChar == '-':
                            assert False, 'Found - char in line at row={row}, col={col}'
                        elif mapChar == '|':
                            crossings += 1
                        else:
                            assert False, 'Unexpected char in line at row={row}, col={col}'
                
        return answer
    
if __name__ == '__main__':
    problem = DayXX()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



