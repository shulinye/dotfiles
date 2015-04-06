#!/usr/bin/python3

import sys

tasks = set()
done = set()
f = []

divider = "Tasks Completed"

class TaskItem(object):
    """A class for tasks that's nestable."""
    def __init__(self, task, *args):
        self.task=task
        self.subtasks=set(TaskItem(i) for i in args)
    def join(self, other):
        assert self.task == other.task
        newTask = TaskItem(self.task)
        newTask.subtasks = self.subtasks.symmetric_difference(other.subtasks)
        intersect = self.subtasks.intersection(other.subtasks)
        if intersect:
            listme = list(self.subtasks)
            listyou = list(other.subtasks)
            for i in listme:
                if i in intersect:
                    j = listyou[listyou.index(i)]
                    newTask.subtasks.add(i.join(j))
        return newTask
    def display(self):
        return "\n".join([self.task] + [str(i) for i in self.subtasks])
    def __repr__(self):
        return self.task
    def __lt__(self, other):
        return self.task < other.task
    def __eq__(self, other):
        return self.task == other.task
    def __hash__(self):
        return hash(self.task)

def makeparagraphs(intake):
    out = []
    for line in intake:
        if "\t" in line: out[-1] += line
        elif line.strip() =='': pass
        else:
            out.append(line)
    return (i for i in out)

paragraphs = makeparagraphs(sys.stdin)

for line in paragraphs:
    if "[ ]" in line:
        task = TaskItem(*line.split('\n'))
        if task not in tasks:
            f.append(task)
            tasks.add(task)
        else:
            n = f.index(task)
            f[n] = f[n].join(task)
    elif "[*]" in line:
        done.add(line)
    elif divider in line:
        break
    elif "" == line.strip():
        pass
    else: f.append(TaskItem(line))

f.append("==== %s ====\n" % divider)

f += list(done)

for line in paragraphs: f.append(line)

for i in f:
    if type(i) == TaskItem:
        print(i.display())
    else:
        print(i)
