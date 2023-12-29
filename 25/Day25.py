#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import copy
import numpy as np

class Day25:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day25')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.nodes = set()
        self.connections = []
        for line in self.lines:
            names = line.replace(':', '').split()
            self.nodes.update(names)
            name = names[0]
            for name2 in names[1:]:
                self.connections.append((min(name, name2), max(name, name2)))

        self.all: dict[str, set[str]] = {}
        for conn in self.connections:
            self.all.setdefault(conn[0], set()).add(conn[1])
            self.all.setdefault(conn[1], set()).add(conn[0])

        self.connections.sort()


    def Part1(self):
        answer = 0
        with open(self.input + ".dot", 'w') as dot:
            print('strict graph Day25 {', file=dot)
            for connection in self.connections:
                print(f'  {connection[0]} -- {connection[1]}', file=dot)
            print('}', file=dot)

        print(f'run:')
        print(f'  neato -Tpdf {self.input}.dot -o {self.input}.pdf')
        print(f'then look at the PDf and enter the nodes on either side')
        print(f'of the edges to be cut.')
        cut1, cut2, cut3 = 'ssd xqh', 'nrs khn', 'qlc mqb'
        # cut1 = input("Enter names of the first 2 nodes whose edge should be cut:  ")
        # cut2 = input("Enter names of the second 2 nodes whose edge should be cut: ")
        # cut3 = input("Enter names of the third 2 nodes whose edge should be cut:  ")

        conn1 = tuple(sorted(cut1.split()))
        conn2 = tuple(sorted(cut2.split()))
        conn3 = tuple(sorted(cut3.split()))

        setNotB = set(c[0] for c in (conn1, conn2, conn3))
        setNotA = set(c[1] for c in (conn1, conn2, conn3))

        all = copy.deepcopy(self.all)
        for c in (conn1, conn2, conn3):
            all[c[0]].remove(c[1])
            all[c[1]].remove(c[0])

        setA = self.Collect(all, conn1[0])
        setB = self.Collect(all, conn1[1])

        assert not setA.intersection(setB), "Sets A and B overlap!"

        print(f'Len of set containing {conn1[0]} is {len(setA)}')
        print(f'Len of set containing {conn1[1]} is {len(setB)}')
        answer = len(setA) * len(setB)

        return answer
    
    def Collect(self, all: dict[str, set[str]], node: str):
        result = set()
        todo = set([node])
        while todo:
            new = todo - result
            if not new:
                break
            result.update(new)
            todo.clear()
            for node in new:
                todo.update(all[node])
        return result

    def Part2(self):
        answer = 0
        return answer
    
if __name__ == '__main__':
    problem = Day25()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



