#!/usr/bin/python3

import os
import re
import shutil
import sys
import tempfile

DIVIDER = 'Tasks Completed'

class TaskItem(object):
    """A class for tasks that's nestable."""
    re_detab = re.compile(r'^\t')
    def __init__(self, tasks_paragraph):
        tasks = tasks_paragraph.split('\n')
        self.task = tasks[0].rstrip()
        if len(tasks) > 1:
            paragraphs = self.make_paragraphs(self.re_detab.sub('', i) for i in tasks[1:])
            self.subtasks = set(TaskItem(i) for i in paragraphs if i != '')
        else:
            self.subtasks = set()
    def join(self, other):
        if self.task != other.task: raise ValueError
        newTask = TaskItem(self.task)
        newTask.subtasks = self.subtasks.symmetric_difference(other.subtasks)
        intersect = self.subtasks.intersection(other.subtasks)
        if intersect:
            dict_me = {i.task: i for i in self.subtasks}
            dict_you = {i.task: i for i in other.subtasks}
            for k, v in dict_me.items():
                if v in intersect:
                    j = dict_you[k]
                    newTask.subtasks.add(v.join(j))
        return newTask
    def display(self):
        return "\n".join([self.task] + ['\t' + i.display() for i in self.subtasks])
    def __repr__(self):
        return self.task
    def __lt__(self, other):
        return self.task < other.task
    def __eq__(self, other):
        return self.task == other.task
    def __hash__(self):
        return hash(self.task)

    @staticmethod
    def make_paragraphs(infile):
        out = []
        for line in infile:
            if line.strip() == '':
                continue
            elif '\t' in line:
                out[-1] += line
            else:
                out.append(line)
        return (i for i in out)

def make_tasks(paragraphs, divider = DIVIDER):
    tasks = set()
    done = set()
    out = []

    for line in paragraphs:
        if '' == line.strip():
            continue
        elif '[ ]' in line:
            task = TaskItem(line)
            if task not in tasks:
                out.append(task)
                tasks.add(task)
            else:
                n = out.index(task)
                out[n] = output[n].join(task)
        elif '[*]' in line:
            done.add(line)
        elif divider in line:
            break
        else: out.append(line.rstrip())

    out.append('==== %s ====\n' % divider)
    out += list(done)
    for line in paragraphs: out.append(line)
    return out

def display_tasks(out, outfile = sys.stdout):
    for i in out:
        if isinstance(i, TaskItem):
            outfile.write(i.display() + '\n\n')
        else:
            outfile.write(i + '\n')

def open_infile(infile_name=None):
    if infile_name is None:
        return sys.stdin
    else:
        return open(infile_name)

def open_outfile(infile_name=None, outfile_name=None, in_place = False):
    if in_place or infile_name == outfile_name:
        outfile = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        path = outfile.name
        return outfile, path
    if outfile_name is None:
        outfile = sys.stdout
    else:
        outfile = open(outfile_name)
    return outfile, None

def main(infile_name = None, outfile_name = None, in_place = False, divider = DIVIDER):
    try:
        infile = open_infile(infile_name)
        paragraphs = TaskItem.make_paragraphs(infile)
    finally:
        if infile != sys.stdin:
            infile.close()
    out = make_tasks(paragraphs, divider)
    try:
        outfile, tmppath = open_outfile(infile_name, outfile_name, in_place)
        display_tasks(out, outfile)
    finally:
        if outfile != sys.stdout:
            outfile.close()
    if tmppath:
        shutil.copy(tmppath, infile_name)
        os.remove(tmppath)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=str, default=None)
    parser.add_argument('outfile', nargs='?', type=str, default=None)
    #in-place option? Switch infile and outfile into strings so I can validate and then open files myself? Something with tempfiles?
    parser.add_argument('-i', '--in-place', help='Output file. Default is stdout', action="store_true")
    parser.add_argument('-d', '--divider', default=DIVIDER)
    args = parser.parse_args()
    main(infile_name=args.infile, outfile_name=args.outfile, in_place=args.in_place, divider=args.divider)
