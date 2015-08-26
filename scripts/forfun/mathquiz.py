#/usr/bin/env python3

import operator
import random
import signal
from time import sleep

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

def ask_question(timeout=TIMEOUT):
    a,b,c = [random.randint(10) for _ in range(3)]
    op1, op2 = random.sample(list(mapping),2)
    ans = mapping[op2](mapping[op1](a,b), c)
    try:
        prompt = "(%d %s %d) %s %d = " % (a, op1, b, op2, c)
        userans = input_with_timeout(prompt, timeout)
        if "exit" in userans: raise KeyboardInterrupt
        if abs(ans - float(userans)) < 0.001:
            print("Correct!")
            return True
    except TimeoutError:
        print("\nTimed out: answer was", ans)
        raise
    except ValueError:
        print("Invalid input: answer was", ans)
        raise
    else:
        print("Incorrect: answer is", ans)

def main(timeout=TIMEOUT):
    score = 0
    incorrect = 0
    timedout_count = 0
    try:
        while True:
            try:
                if ask_question(timeout=TIMEOUT):
                    score += 1
                else:
                    incorrect += 1
            except TimeoutError:
                timedout_count += 1
            except ValueError:
                pass
            except ZeroDivisionError:
                pass
            sleep(0.1)
    except KeyboardInterrupt:
        print('\nCorrect answers: {}\nIncorrect: {}\nTimed out: {}'.format(score, incorrect, timedout_count))

if __name__ == "__main__":
    import sys
    if len(sys.argv) >1 : main(float(sys.argv[1]))
    else: main()
