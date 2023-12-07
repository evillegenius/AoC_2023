#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import collections

# Mnemonic hand ranks
rankHighCard = 1
rankOnePair = 2
rankTwoPairs = 3
rankThreeOfAKind = 4
rankFullHouse = 5
rankFourOfAKind = 6
rankFiveOfAKind = 7

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
        maxCount = counts[0]
        if maxCount == 1:
            return (rankHighCard, hand) # high card
        if maxCount == 5:
            return (rankFiveOfAKind, hand) # 5 of a kind
        if maxCount == 4:
            return (rankFourOfAKind, hand) # 4 of a kind
        if maxCount == 3:
            if counts[1] == 2:
                return (rankFullHouse, hand) # full house
            else:
                return (rankThreeOfAKind, hand) # 3 of a kind)
        if maxCount == 2:
            if counts[1] == 2:
                return (rankTwoPairs, hand) # 2 pair
            else:
                return (rankOnePair, hand) # 1 pair
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

        if counts == [5]:
            return (rankFiveOfAKind, hand)

        if counts == [4, 1]:
            if jokers:
                return (rankFiveOfAKind, hand)
            else:
                return (rankFourOfAKind, hand)

        if counts == [3, 2]:
            if jokers:
                return (rankFiveOfAKind, hand)
            else:
                return (rankFullHouse, hand)
            
        if counts == [3, 1, 1]:
            if jokers:
                return (rankFourOfAKind, hand)
            else:
                return (rankThreeOfAKind, hand)
            
        if counts == [2, 2, 1]:
            if jokers == 2:
                return (rankFourOfAKind, hand)
            elif jokers == 1:
                return (rankFullHouse, hand)
            else:
                return (rankTwoPairs, hand)
            
        if counts == [2, 1, 1, 1]:
            if jokers:
                return (rankThreeOfAKind, hand)
            else:
                return (rankOnePair, hand)

        if counts == [1, 1, 1, 1, 1]:
            if jokers:
                return (rankOnePair, hand)
            else:
                return (rankHighCard, hand)
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



