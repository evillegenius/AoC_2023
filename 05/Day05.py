#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
from collections import namedtuple

# An interval represents the range [begin .. end)
class Interval(namedtuple('Interval', ['begin', 'end'])):
    def __bool__(self):
        # Invalid intervals evaluate as False
        return self.begin < self.end
    
    def __add__(self, offset):
        return Interval(self[0] + offset, self[1] + offset)
    
    def SplitAgainst(self, other):
        return (Interval(self.begin, min(self.end, other.begin)),
                Interval(max(self.begin, other.begin), min(self.end, other.end)),
                Interval(max(self.begin, other.end), self.end))


class Day05:
    def __init__(self):
        self.input = None

        self.lines = []
        self.seeds = []
        self.maps = {}
        self.seedToSoil = {}
        self.soilToFertilizer = {}
        self.fertilizerToWater = {}
        self.waterToLight = {}
        self.lightToTemp = {}
        self.tempToHumidity = {}
        self.humidityToLocation = {}
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day05')
        parser.add_argument('input', nargs='?', default='input.txt')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Part1(self):
        mapName = None
        for line in self.lines:
            if line.startswith('seeds:'):
                seeds = [int(seed) for seed in line.split(':')[-1].split()]
                continue
            elif line.endswith(' map:'):
                mapName = line[:-5]
                seedMap = []
            else:
                parts = line.split()
                if len(parts) == 3:
                    dst, src, length = [int(part) for part in parts]
                    seedMap.append((src, dst, length))
                    continue
                if not mapName:
                    continue
                self.DoMapSeeds(mapName, seedMap, seeds)
                seedMap = []

        if seedMap:
            self.DoMapSeeds(mapName, seedMap, seeds)        


        answer = min(seeds)
            
        return answer
    
    def DoMapSeeds(self, mapName, seedMap, seeds):
        "Modifies seeds in-place"
        seedMap.sort()

        for i, seed in enumerate(seeds):
            prev = seed
            for src, dst, length in seedMap:
                if src > seed:
                    break
                if src <= seed < src + length:
                    seeds[i] = seed - src + dst
                    break
            # print(f'{prev} -> {mapName} -> {seeds[i]}')

    def Part2(self):
        seeds = [int(seed)
                 for seed in self.lines[0].split(':')[-1].split()]
        seedInts = [Interval(seeds[i], seeds[i] + seeds[i+1])
                    for i in range(0, len(seeds), 2)]

        mapName = None
        for line in self.lines[2:]:
            if line.endswith(' map:'):
                mapName = line[:-5]
                seedMap = []
            else:
                parts = line.split()
                if len(parts) == 3:
                    dst, src, length = [int(part) for part in parts]
                    seedMap.append((Interval(src, src + length), dst - src))
                    continue
                if not mapName:
                    continue
                seedInts = self.DoMapSeedInts(mapName, seedMap, seedInts)
                seedMap = []

        if seedMap:
            seedInts = self.DoMapSeedInts(mapName, seedMap, seedInts)        

        answer = min(pair[0] for pair in seedInts)
            
        return answer

    def DoMapSeedInts(self, mapName, seedMap, seedInts):
        seedInts = sorted(seedInts, reverse=True)
        seedMap = sorted(seedMap, reverse=True)

        # print(f'{mapName}:')
        # print(f'  Seeds:')
        # for item in seedInts:
        #     print(f'    {item}')
        # print(f'  Mappings:')
        # for srcInt, offset in seedMap:
        #     print(f'    {srcInt}, {offset}')

        result = []
        count = 0
        srcInt, offset = seedMap.pop()
        seedInt = seedInts.pop()
        try:
            while True:
                before, during, after = seedInt.SplitAgainst(srcInt)
                if before:
                    result.append(before)
                if during:
                    result.append(during + offset)
                if after:
                    srcInt, offset = seedMap.pop()
                    seedInt = after
                else:
                    seedInt = seedInts.pop()

        except IndexError:
            if after:
                result.append(after)
            result.extend(reversed(seedInts))

        # print(f'  Returns:')
        # for item in result:
        #     print(f'    {item})')

        return result

if __name__ == '__main__':
    problem = Day05()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



