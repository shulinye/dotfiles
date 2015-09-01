#/usr/bin/env python3

from fractions import Fraction
import operator
import random
import signal
from time import sleep

mapping = {'+': operator.add,
           '*': operator.mul,
           '-': operator.sub,
           '/': operator.truediv}

operators = list(mapping)
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

def ask_question(timeout=TIMEOUT):
    a,b,c = [Fraction(random.randint(0,10),1) for _ in range(3)]
    op1, op2 = random.sample(operators,2)
    ans = mapping[op2](mapping[op1](a,b), c)
    try:
        prompt = "(%d %s %d) %s %d = " % (a, op1, b, op2, c)
        while True:
            try:
                userans = input_with_timeout(prompt, timeout)
                if "exit" in userans: raise KeyboardInterrupt
                userans = Fraction(userans)
                break
            except ValueError:
                print("Invalid input.")
                continue
        if abs(ans - userans) < 0.001:
            print("Correct!")
            return True
    except TimeoutError:
        print("\nTimed out: answer was", ans)
        raise
    else:
        print("Incorrect: answer is", ans)

def main(timeout=TIMEOUT):
    score = 0
    incorrect = 0
    timedout_count = 0
    question_count = 0
    try:
        while True:
            try:
                if ask_question(timeout=timeout):
                    score += 1
                else:
                    incorrect += 1
            except TimeoutError:
                timedout_count += 1
            except ZeroDivisionError:
                continue
            sleep(0.1)
            question_count += 1
    except KeyboardInterrupt:
        print('\n--------\nCorrect answers: {}\nIncorrect: {}\nTimed out: {}\nTotal Questions: {}'.format(score, incorrect, timedout_count, question_count))

if __name__ == "__main__":
    import sys
    if len(sys.argv) >1 : main(int(sys.argv[1]))
    else: main()
