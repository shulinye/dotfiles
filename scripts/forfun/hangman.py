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
        if self.status >= 6: raise ValueError("Dead")
        self.status += 1
        return self.hangman[:1 + self.status] + [self.empty]*(6-self.status) + [self.end]
    def display(self):
        print("\n".join(self.output()))
