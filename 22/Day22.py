#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np
from collections import namedtuple
from dataclasses import dataclass

@dataclass
class Block:
    x0: int
    y0: int
    z0: int

    x1: int
    y1: int
    z1: int

    id: int = -1

    def __post_init__(self):
        assert self.x0 <= self.x1
        assert self.y0 <= self.y1
        assert self.z0 <= self.z1

        self.drop = 0  # How far does this block drop
        self.fall = set() # Set of blocks that would fall
        self.below = set()  # block ids below me
        self.above = set()  # block ids above me
        self.safe = True # Safe to disintegrate this block?

    def __str__(self):
        return f"{self.x0},{self.y0},{self.z0-self.drop}~{self.x1},{self.y1},{self.z1-self.drop}   <- {self.id} above({sorted(self.below)})"

    
class Day22:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day22')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.blocks = []
        for line in self.lines:
            coords = list(map(int, line.replace('~', ',').split(',')))
            self.blocks.append(Block(*coords, id=len(self.blocks)))
        
        minX = min(b.x0 for b in self.blocks)
        maxX = max(b.x1 for b in self.blocks)
        minY = min(b.y0 for b in self.blocks)
        maxY = max(b.y1 for b in self.blocks)

        print(f'read {len(self.blocks)} blocks')
        print(f'xRange = {minX} .. {maxX}')
        print(f'yRange = {minY} .. {maxY}')

        self.width = (maxX - minX) + 1
        self.height = (maxY - minY) + 1

        # ########################################################################
        # # If the puzzle is not grid/map based, delete these lines.
        # gridKey = {'.': 0, '#': 1, 'O': 2}
        # self.height = len(self.lines)
        # self.width = len(self.lines[0])

        # self.grid = np.zeros((self.height, self.width), dtype=int)
        # for row, line in enumerate(self.lines):
        #     for col, ch in enumerate(line):
        #         self.grid[row, col] = gridKey[ch]
        # #
        # ########################################################################


    def Part1(self):
        answer = 0
        # heights is a map of height and id of the block at that height
        heights = np.zeros((self.width, self.height, 2), dtype=int)
        heights[:, :, 1] = -1  # set ids to -1

        # Get a shorter to type handle on the blocks
        blocks = self.blocks

        ByZ0 = lambda block: block.z0

        # Traverse them from the bottom up and drop them onto the height map.
        for block in sorted(blocks, key=ByZ0):
            heightView = heights[block.x0:block.x1+1, block.y0:block.y1+1, 0]
            idView = heights[block.x0:block.x1+1, block.y0:block.y1+1, 1]
            heightMax = heightView.max()
            maxIndices = np.nonzero(heightView == heightMax)
            ids = set(idView[maxIndices].flat)
            ids.discard(-1)
            block.below = ids
            for id in ids:
                blocks[id].above.add(block.id)

            drop = block.z0 - heightMax - 1
            assert drop >= 0
            block.drop = drop # XXX not sure I need to save this
            hNew = block.z1 - drop

            heightView[...] = hNew
            idView[...] = block.id

            # print("=" * 20)
            # print(block)
            # print(heights)

        for block in blocks:
            for id in block.above:
                if len(blocks[id].below) == 1:
                    block.safe = False
                    break
            else:
                print(f'Can disintegrate {block}')
                block.safe = True
                answer += 1

        return answer

    def Chain(self, block:Block, falling:set[int]):
        for id in block.above:
            if not (self.blocks[id].below - falling):
                # everything below this block is falling
                falling.add(id)
                self.Chain(self.blocks[id], falling)


    def Part2(self):
        answer = 0
        blocks = self.blocks

        for block in blocks:
            if block.safe:
                # This one won't cause a chain reaction on its own
                continue

            falling = set([block.id])
            self.Chain(block, falling)
            answer += len(falling) - 1 # Subtract 1 to exclude block itself

        return answer
    
if __name__ == '__main__':
    problem = Day22()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



