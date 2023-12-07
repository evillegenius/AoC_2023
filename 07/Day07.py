#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import collections

class Day07:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day07')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Score(self, game):
        hand, bid = game
        cards = collections.Counter()
        hand = hand.replace('T', 'a').replace('J', 'b').replace('Q', 'c').replace('K', 'd').replace('A', 'e')        
        cards.update(hand)
        common = cards.most_common()
        counts = [item[1] for item in common]
        maxCount = max(counts)
        if maxCount == 1:
            return (1, hand) # high card
        if maxCount == 5:
            return (7, hand) # 5 of a kind
        if maxCount == 4:
            return (6, hand) # 4 of a kind
        if maxCount == 3:
            if counts[1] == 2:
                return (5, hand) # full house
            else:
                return (4, hand) # 3 of a kind)
        if maxCount == 2:
            if counts[1] == 2:
                return (3, hand) # 2 pair
            else:
                return (2, hand) # 1 pair
        assert False, f"Hand failed ranking {game}"

    def Part1(self):
        games = [line.split() for line in self.lines]
        games.sort(key=self.Score)
        answer = 0
        for i, (hand, bid) in enumerate(games):
            answer += (i + 1) * int(bid)
        return answer

    def Score2(self, game):
        hand, bid = game
        cards = collections.Counter()
        hand = hand.replace('T', 'a').replace('J', '0').replace('Q', 'c').replace('K', 'd').replace('A', 'e')
        cards.update(hand)
        common = cards.most_common()
        counts = [item[1] for item in common]
        jokers = cards['0']

        maxCount = max(counts)
        if maxCount == 1:
            return (1 + jokers, hand) # high card
        if maxCount == 5:
            return (7, hand) # 5 of a kind
        if maxCount == 4:
            if common[0][0] == '0':
                return (7, hand) # 5 of a kind
            else:
                return (6 + jokers, hand) # 4 of a kind
        if maxCount == 3:
            if common[0][0] == '0':
                return (5 + counts[1], hand)
            if jokers:
                return(5 + jokers, hand)
            if counts[1] == 2:
                return (5, hand) # full house
            else:
                return (4, hand) # 3 of a kind)
        if maxCount == 2:
            if jokers == 1:
                if counts == [2, 2, 1]:
                    return (5, hand) # full house
                else:
                    return (4, hand) # 3 of a kind
                assert False, f'Bad joker count: {game}'
            if jokers == 2:
                if counts == [2, 2, 1]:
                    return (6, hand) # 4 of a kind
                else:
                    return (4, hand) # 3 of a kind
                assert False, f'Another bad joker count: {game}'
            if counts[1] == 2:
                return (3, hand) # 2 pair
            else:
                return (2, hand) # 1 pair
        assert False, f"Hand failed ranking {game}"

    def Part2(self):
        games = [line.split() for line in self.lines]
        games.sort(key=self.Score2)
        answer = 0
        for i, (hand, bid) in enumerate(games):
            answer += (i + 1) * int(bid)
        return answer
    
if __name__ == '__main__':
    problem = Day07()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



