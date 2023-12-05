#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys

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
        mapNames = ("seed-to-soil soil-to-fertilizer fertilizer-to-water"
                    " water-to-light light-to-temperature temperature-to-humidity"
                    " humidity-to-location").split()

        answer = 99999999999
        mapName = ""
        for line in self.lines:
            if line.startswith('seeds:'):
                self.seeds = [int(seed) for seed in line.split(':')[-1].split()]
            elif line.endswith(' map:'):
                mapName = line[:-5]
            else:
                parts = line.split()
                if len(parts) != 3:
                    continue
                dst, src, length = [int(part) for part in parts]
                m = self.maps.setdefault(mapName, {})
                for i in range(length):
                    m[src + i] = dst + i

        for seed in self.seeds:
            for mapName in mapNames:
                prev = seed
                seed = self.maps[mapName].get(seed, seed)
                print(f'{prev} -> {mapName} -> {seed}')
            
            answer = min(seed, answer)

            
        return answer
    

    def Part2(self):
        answer = 0
        return answer
    
if __name__ == '__main__':
    problem = Day05()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



