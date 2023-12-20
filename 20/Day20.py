#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
from typing import Optional
from collections import deque
import re
import math

LOW = 0
HIGH = 1

pulseName = ["low", "high"]

class Node:
    signals = deque()
    nodes = {}
    counts = [0, 0]
    pushes = 0
    cycles = {}

    @classmethod
    def ResetAll(cls):
        Node.counts = [0, 0]
        Node.pushes = 0

        for node in cls.nodes.values():
            node.Reset()

    @classmethod
    def SetupDebug(cls):
        definedNodes = set(cls.nodes)
        allNodes = set()
        for node in cls.nodes.values():
            allNodes.update(node.outputs)

        debugNodes = allNodes - definedNodes
        for name in debugNodes:
            _ = Debug(name)

    @classmethod
    def SetupInputs(cls):
        for name, node in cls.nodes.items():
            for dst in node.outputs:
                cls.nodes[dst].AddInput(name)

    def __init__(self, name: str, outputs: list[str]):
        self.name = name
        self.outputs = outputs
        self.inputs = []
        self.id = len(self.nodes)
        self.nodes[name] = self
        self.debug = 0
        self.cycleCount = None

    def AddInput(self, name:str):
        self.inputs.append(name)

    def Send(self, pulse: int, dst:str):
        self.signals.appendleft((pulse, self.name, dst))

    def SendAll(self, pulse:int):
        for dst in self.outputs:
            self.Send(pulse, dst)

    def Receive(self, pulse:int, src:str):
        raise NotImplementedError

    def Reset(self):
        pass    

class Button(Node):

    def __init__(self):
        super().__init__('button', ['broadcaster'])

    def Push(self):
        Node.pushes += 1
        self.Send(LOW, "broadcaster")
        while self.signals:
            (pulse, src, dst) = self.signals.pop()

            # print(f'{src} -{pulseName[pulse]}-> {dst}')
            self.counts[pulse] += 1
            self.nodes[dst].Receive(pulse, src)


class Debug(Node):
    def __init__(self, name:str):
        super().__init__(name, [])

    def Receive(self, pulse:int, src:str):
        if self.debug:
            self.debug -= 1
            print(f'{self.name} Received {pulseName[pulse]}')


class Broadcast(Node):
    def __init__(self, name:str, outputs:list[str]):
        super().__init__(name, outputs)

    def Receive(self, pulse:int, src:str):
        self.SendAll(pulse)


class FlipFlop(Node):
    def __init__(self, name:str, outputs:list[str]):
        super().__init__(name, outputs)
        self.state = False

    def Reset(self):
        self.state = False

    def Receive(self, pulse:int, src:str):
        if pulse == HIGH:
            return

        self.state = not self.state
        # print(f'    {self.name}: ON')
        self.SendAll(HIGH if self.state else LOW)

class Conjunction(Node):
    def __init__(self, name:str, outputs:list[str]):
        super().__init__(name, outputs)
        self.state = {}

    def Reset(self):
        for input in self.state:
            self.state[input] = LOW

    def Receive(self, pulse:int, src:str):
        self.state[src] = pulse
        # print(f'    {self.name}: {src} now {pulseName[pulse]}')
        toSend = LOW if all(self.state.values()) else HIGH

        if self.debug and toSend == HIGH:
            if self.cycleCount is None:
                self.cycleCount = Node.pushes
                print(f'{self.name}: pushes={Node.pushes}, sending {pulseName[toSend]}')
            else:
                if self.cycleCount * 2 != Node.pushes:
                    print(f'ERROR: {Node.pushes}: Uneven cycles for {self.name},'
                          f' {self.cycleCount} vs {Node.pushes - self.cycleCount}')
                Node.cycles[self.name] = self.cycleCount
                self.debug = 0
                Node.pending -= 1

        self.SendAll(toSend)

    def AddInput(self, name):
        super().AddInput(name)
        self.state[name] = LOW


class Day20:
    def __init__(self):
        self.input = None

        self.button = None

        self.lines = []

        self.nodePat = re.compile(r'^([%&]?)(\w+) -> (.*)$')
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day20')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

    def Part1(self):
        answer = 0
        for line in self.lines:
            match = self.nodePat.match(line)
            assert match, f"Line {line!r} failed to match"

            self.button = Button()

            typ, name, dests = match.groups()
            dests = dests.split(', ')
            if not typ:
                node = Broadcast(name, dests)
            elif typ == '%':
                node = FlipFlop(name, dests)
            elif typ == '&':
                node = Conjunction(name, dests)

        self.button.SetupDebug()
        self.button.SetupInputs()

        for _ in range(1000):
            self.button.Push()

        print(f'Counts = {self.button.counts}')
        answer = self.button.counts[0] * self.button.counts[1]

        return answer


    def Part2(self):
        self.button.ResetAll()

        # Having determined by inspecting the input that
        # rx will get a low signal when all the inputs to hj
        # are producing high signals. Debug them to see when
        # they cycle.
        
        hj = self.button.nodes['hj']
        for input in hj.inputs:
            Node.cycles[input] = 0
            node = self.button.nodes[input]
            node.debug = 1
        Node.pending = len(hj.inputs)

        while Node.pending:
            self.button.Push()

        answer = math.lcm(*Node.cycles.values())

        return answer
    
if __name__ == '__main__':
    problem = Day20()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



