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

"""--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

    .....
    .F-7.
    .|.|.
    .L-J.
    .....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

    .....
    .S-7.
    .|.|.
    .L-J.
    .....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

    -L|F7
    7S-7|
    L|7||
    -L-J|
    L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

    7-F7-
    .FJ|7
    SJLL7
    |F--J
    LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

    .....
    .S-7.
    .|.|.
    .L-J.
    .....

You can count the distance each tile in the loop is from the starting point like this:

    .....
    .012.
    .1.3.
    .234.
    .....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...

Here are the distances for each tile on that loop:

    ..45.
    .236.
    01.78
    14567
    23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

Your puzzle answer was 6757.

--- Part Two ---
You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

    ...........
    .S-------7.
    .|F-----7|.
    .||.....||.
    .||.....||.
    .|L-7.F-J|.
    .|..|.|..|.
    .L--J.L--J.
    ...........

The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

    ...........
    .S-------7.
    .|F-----7|.
    .||OOOOO||.
    .||OOOOO||.
    .|L-7OF-J|.
    .|II|O|II|.
    .L--JOL--J.
    .....O.....

In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

    ..........
    .S------7.
    .|F----7|.
    .||OOOO||.
    .||OOOO||.
    .|L-7F-J|.
    .|II||II|.
    .L--JL--J.
    ..........

In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

    .F----7F7F7F7F-7....
    .|F--7||||||||FJ....
    .||.FJ||||||||L7....
    FJL7L7LJLJ||LJ.L-7..
    L--J.L7...LJS7F-7L7.
    ....F-J..F7FJ|L7L7L7
    ....L7.F7||L7|.L7L7|
    .....|FJLJ|FJ|F7|.LJ
    ....FJL-7.||.||||...
    ....L---J.LJ.LJLJ...

The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

    OF----7F7F7F7F-7OOOO
    O|F--7||||||||FJOOOO
    O||OFJ||||||||L7OOOO
    FJL7L7LJLJ||LJIL-7OO
    L--JOL7IIILJS7F-7L7O
    OOOOF-JIIF7FJ|L7L7L7
    OOOOL7IF7||L7|IL7L7|
    OOOOO|FJLJ|FJ|F7|OLJ
    OOOOFJL-7O||O||||OOO
    OOOOL---JOLJOLJLJOOO

In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?

Your puzzle answer was 523.
"""

