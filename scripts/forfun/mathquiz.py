#/usr/bin/env python3

import operator
import random
import signal
from decimal import Decimal, InvalidOperation

mapping = {'+': operator.add,
           '*': operator.mul,
           '-': operator.sub,
           '/': operator.truediv}

TIMEOUT = 10

def handler(signum, frame):
    raise TimeoutError

def input_with_timeout(prompt, timeout=TIMEOUT):
    old_handler = signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    try:
        return input(prompt)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

def ask_question():
    a,b,c = [random.randint(1,10) for _ in range(3)]
    op1, op2 = random.sample(list(mapping),2)
    ans = mapping[op2](mapping[op1](*map(Decimal,(a,b))), Decimal(c))
    try:
        prompt = "(%d %s %d) %s %d = " % (a, op1, b, op2, c)
        if ans == Decimal(input_with_timeout(prompt)):
            print("Correct!")
            return True
    except TimeoutError:
        print("\nTimed out: answer was", ans)
    except InvalidOperation:
        print("Invalid input: answer was", ans)
    else:
        print("Incorrect: answer is", ans)

def main():
    score = 0
    try:
        while True:
            if ask_question():
                score += 1
    except KeyboardInterrupt:
        print('\nCorrect answers:',score)

if __name__ == "__main__":
    main()

