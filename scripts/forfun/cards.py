#!/usr/bin/python3

"""A deck of playing cards"""

import sys
from os import path

if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.realpath(__file__))))

from random import shuffle
from collections import deque
from itertools import product

__all__ = ['Card', 'Deck']

from functools import total_ordering
from pythonutils import autoinit, autorepr

@total_ordering
@autorepr
@autoinit
class Card(object):
    """Virtual playing card"""
    suit_map = ['Clubs','Diamonds', 'Hearts', 'Spades']
    rank_map = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    __slots__ = ('suit', 'rank')
    def __str__(self):
        return '<%s: %s of %s>' % (self.__class__.__name__, self.rank_map[self.rank], self.suit_map[self.suit])
    def __eq__(self, other):
        if not isinstance(other, Card): return False
        return self.suit == other.suit and self.rank == other.rank
    def __lt__(self, other):
        if not isinstance(other, Card):
            raise TypeError("unorderable types, %s < %s" % (type(self).__name__, type(other).__name__))
        if self.rank == other.rank:
            return self.suit < other.suit
        if self.rank == 0: # I have an Ace!
            return False
        if other.rank == 0: # They have an Ace!
            return True
        return self.rank < other.rank

class Deck(deque):
    """A deck of cards. Uses python's deque"""
    def __init__(self, cards = None, decks = 1):
        li = [] #temporary list, to make shuffling more effective.
        if cards is None:
            for i,j,_ in product(range(4), range(13), range(decks)):
                li.append(Card(i,j))
        else:
            li.extend(cards)
        shuffle(li)
        self.extend(li)
    def deal(self, pile_count : int = 2, card_count = None):
        """Deals out deck into seperate piles"""
        hands = [Deck([]) for _ in range(pile_count)]
        if card_count is None:
            card_count = len(self)//pile_count + 1
        try:
            for _ in range(card_count):
                for i in hands:
                    i.appendleft(super().popleft())
        except IndexError:
            pass
        return hands
    def shuffle(self):
        """Shuffles deck, using random.shuffle
        (and a temporary list, for performance reasons)"""
        li = list(self)
        shuffle(li)
        self.clear()
        self.extend(li)
    def popleft(self, n = 1):
        return [super(Deck, self).popleft() for _ in range(n)]
    def pop(self, n = 1):
        return [super(Deck, self).pop() for _ in range(n)]
    def __str__(self):
        return 'deque([%s])' % ', '.join(map(str,self))
