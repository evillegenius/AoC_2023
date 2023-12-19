#!/usr/bin/env python3
"""
<Problem description here>
"""
import re
from collections import namedtuple

class Interval(namedtuple('Interval', 'start stop')):
    def __bool__(self):
        return self.start < self.stop
    
    def Split(self, op, value):
        if op == '>':
            value += 1
        below = Interval(self.start, min(self.stop, value))
        above = Interval(max(self.start, value), self.stop)

        if op == '<':
            return below, above
        elif op == '>':
            return above, below
        else:
            assert False, f'Unrecognized op value {op!r}'

    def __len__(self):
        return max(0, self.stop - self.start)

    def __iter__(self):
        return range(self.start, self.stop)

class Intervals(namedtuple('Intervals', 'x m a s')):
    def __bool__(self):
        return bool(self.x) or bool(self.m) or bool(self.a) or bool(self.s)
    
    def Count(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)
    
    def Split(self, attr, op, value):
        if attr == 'x':
            x1, x2 = self.x.Split(op, value)
            return self._replace(x=x1), self._replace(x=x2)
        elif attr == 'm':
            m1, m2 = self.m.Split(op, value)
            return self._replace(m=m1), self._replace(m=m2)
        elif attr == 'a':
            a1, a2 = self.a.Split(op, value)
            return self._replace(a=a1), self._replace(a=a2)
        elif attr == 's':
            s1, s2 = self.s.Split(op, value)
            return self._replace(s=s1), self._replace(s=s2)
        else:
            assert False, f'Unknown attr name {attr!r}'

    def Text(self):
        return (f'I'
                f'(x=[{self.x.start}:{self.x.stop}],'
                f' m=[{self.m.start}:{self.m.stop}],'
                f' a=[{self.a.start}:{self.a.stop}],'
                f' s=[{self.s.start}:{self.s.stop}])')
        

class Day19:
    def __init__(self):
        self.input = None

        self.lines = []

        self.rules = {}
        self.parts = []

        self.rulePat = re.compile(r'^(\w+){([^}]+)}$')
        self.conditionPat = re.compile(r'(([xmas])([<>])(\d+):)?(\w+)')

        self.partPat = re.compile(r'^{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}$')

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day19')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def CodeGen(self):
        result = []
        result.append('def f_A(part):\n'
                      '    return sum(part.values())\n'
                      '\n'
                      'def f_R(part):\n'
                      '    return 0\n')

        for rule, conditions in self.rules.items():
            result.append(f'def f_{rule}(part):')
            for condition in conditions:
                _, category, op, value, target = condition
                if category:
                    result.append(f'    if part["{category}"] {op} {value}:'
                                  f'        return f_{target}(part)')
                else:
                    result.append(f'    return f_{target}(part)')
                    result.append('')
        
        return '\n'.join(result)


    def Part1(self):
        answer = 0

        lineIter = iter(self.lines)
        for line in lineIter:
            if not line:
                break
            match = self.rulePat.match(line)
            assert match, f'line {line!r} failed to match rulePat'
            name, conditions = match.groups()
            self.rules[name] = self.conditionPat.findall(conditions)

        for line in lineIter:
            match = self.partPat.match(line)
            assert match, f'line {line!r} failed to match partPat'
            part = match.groupdict()
            for key in 'xmas':
                part[key] = int(part[key])
            self.parts.append(part)

        codeGen = self.CodeGen()
        # print(codeGen)
        code = compile(codeGen, '-codegen-', 'exec')
        codeDict = {}
        exec(code, codeDict)

        func = codeDict['f_in']

        for part in self.parts:
            value = func(part)
            answer += value
        
        # import pprint
        # pprint.pprint(self.rules)
        # print()
        # pprint.pprint(self.parts)

        return answer

    def Part2(self):
        answer = 0
        full = Interval(1, 4001)
        intervals = Intervals(full, full, full, full)

        todo = []
        todo.append(('in', intervals))
        while todo:
            target, intervals = todo.pop()
            if not intervals:
                continue

            if target == 'A':
                # print('A =', intervals.Text())
                count = intervals.Count()
                answer += count
                continue
            elif target == 'R':
                # print('R =', intervals.Text())
                continue

            conditions = self.rules[target]
            for condition in conditions:
                _, category, op, value, target = condition
                if not category:
                    # This should be the last condition
                    todo.append((target, intervals))
                    break

                # Get the included and excluded intervals
                inc, exc = intervals.Split(category, op, int(value))

                if inc:
                    todo.append((target, inc))

                if not exc:
                    break

                intervals = exc

        return answer
    
if __name__ == '__main__':
    problem = Day19()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



