#!/usr/bin/python3

class Hangman(object):
    hangman = [
            r'|----------|---',
            r'|          |   ',
            r'|          O   ',
            r'|         /|\  ',
            r'|          |   ',
            r'|         / \  ',
            r'|        /   \ ']
    end   = r'|--------------'
    empty = r'|              '
    def __init__(self):
        self.status = 0
    def output(self):
        return self.hangman[:2 + self.status] + [self.empty]*(5-self.status) + [self.end]
    def display(self):
        print("\n".join(self.output()))
    def __iadd__(self, val):
        if self.status >= 5: raise ValueError("Already dead!")
        self.status += val
        return self
