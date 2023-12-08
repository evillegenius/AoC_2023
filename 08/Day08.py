#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import itertools
import re

class Day08:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day08')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.directions = ['LR'.find(c) for c in self.lines[0]]
        assert min(self.directions) == 0, "Bad directions"
        self.network = {}
        for line in self.lines[2:]:
            match = re.match(r'^(...) = .(...), (...).$', line)
            assert match, f'line {line!r} failed to match'

            node, left, right = match.groups()
            self.network[node] = (left, right)

    def Part1(self):
        answer = 0

        node = 'AAA'
        for direction in itertools.cycle(self.directions):
            node = self.network[node][direction]
            answer += 1
            if node == 'ZZZ':
                break

        return answer

    def Part2(self):
        answer = 0
        nodes = [node for node in self.network if node.endswith('A')]
        numNodes = len(nodes)
        counts = [0] * numNodes

        n = 0
        node = nodes[n]
        count = counts[n]
        while True:
            numDir = len(self.directions)
            while node[2] != 'Z':
                node = self.network[node][self.directions[count % numDir]]
                count += 1

            nodes[n] = node
            counts[n] = count

            print(f'counts[{n}] = {count}')
            # print(f'nodes = {nodes}')
            # print(f'counts = {counts}')

            minCount = min(counts)
            maxCount = max(counts)

            if minCount == maxCount:
                break

            n = counts.index(minCount)
            node = nodes[n]
            count = counts[n]

            # Take 1 step
            node = self.network[node][self.directions[count % numDir]]
            count += 1

        answer = minCount
        return answer
    
if __name__ == '__main__':
    problem = Day08()
    
    #answer1 = problem.Part1()
    #print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



