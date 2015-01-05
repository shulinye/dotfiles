#!/usr/bin/python3

import sys

tasks = set()
done = set()
f = []

def makeparagraphs(intake):
    out = []
    for line in intake:
        if "\t" in line: out[-1] += line
        elif line.strip() == '':
            out.append('\n')
        else:
            out.append(line)
    return (i for i in out)

paragraphs = makeparagraphs(sys.stdin)

for line in paragraphs:
    if "[ ]" in line:
        if line not in tasks:
            f.append(line)
            tasks.add(line)
    elif "[*]" in line:
        done.add(line)
    elif "Tasks Completed" in line:
        break
    elif "" == line.strip():
        f.append("\n")
    else: f.append(line)

f.append("==== Tasks Completed ====\n")

f += list(done)

for line in paragraphs: f.append(line)

print("".join(f))
