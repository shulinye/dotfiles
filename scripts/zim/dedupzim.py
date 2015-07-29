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

    def __init__(self, tasks : tuple):
        self.task = tasks[0].rstrip()
        self.subtasks = set()
        if len(tasks) > 1:
            dedented = [self.re_detab.sub('', i) for i in tasks[1:]]
            paragraphs = self.make_paragraphs(self.re_detab.sub('', i) for i in tasks[1:])
            for i in paragraphs:
                self.subtasks.add(TaskItem(i))

    def join(self, other : "TaskItem") -> "TaskItem":
        """Merges two TaskItems that have the same self.task"""
        if self.task != other.task:
            raise ValueError
        newTask = TaskItem((self.task,))
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

    def display(self) -> str:
        return "\n".join([self.task] + ['\t' + i.display() for i in sorted(self.subtasks)])
        # Note: sorting so numbered tasks make sense, also so comments sort above tasks.
        # Conveniently for me, '*' < '['

    def __repr__(self):
        return "TaskItem(%s)" % self.task

    def __lt__(self, other):
        return self.task < other.task

    def __eq__(self, other):
        if not isinstance(other, TaskItem):
            return False
        return self.task == other.task

    def __hash__(self):
        return hash(self.task)

    @staticmethod
    def make_paragraphs(intake):
        out = []
        for line in intake:
            if line.strip() == '':
                continue
            elif '\t' in line:
                out[-1].append(line.rstrip())
            else:
                out.append([line.rstrip()])
        return (tuple(i) for i in out)


def make_tasks(paragraphs, divider=DIVIDER):
    tasks = set()
    done = set()
    titles = set()
    out = []

    for line in paragraphs:
        if line == ('',):
            continue
        elif len(line) == 1 and line[0].startswith('=') and line[0].endswith('='):
            if divider in line[0]: break
            stripped_title = line[0].strip('=')
            if stripped_title in titles:
                continue
            else:
                out.append(('\n' + line[0],)) #restore a title's whitespace
                titles.add(stripped_title)
        elif any('[ ]' in i for i in line):
            task = TaskItem(line)
            if task not in tasks:
                out.append(task)
                tasks.add(task)
            else:
                n = out.index(task)
                out[n] = out[n].join(task)
        elif any('[*]' in i for i in line):
            done.add(line)
        elif any(divider in i for i in line):
            break
        else:
            out.append([i.rstrip() for i in line])

    out.append(['==== %s ====' % divider])
    out += list(done)
    for line in paragraphs:
        out.append(line)
    return out


def display_tasks(out, outfile=sys.stdout):
    for i in out:
        if isinstance(i, TaskItem):
            outfile.write(i.display() + '\n')
        else:
            outfile.write("\n".join(i) + '\n')


def open_infile(infile_name=None):
    """Open input file. Reads from stdin if no
    input file"""
    if infile_name is None:
        return sys.stdin
    else:
        return open(infile_name)


def open_outfile(outfile_name=None, *, in_place=False, infile_name=None):
    """Open output file. If in_place or output file same as input file,
    open tempfile instead. Elif no outfile, output to stdout."""
    if in_place or (outfile_name and infile_name == outfile_name):
        outfile = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        path = outfile.name
        return outfile, path
    if outfile_name is None:
        outfile = sys.stdout
    else:
        outfile = open(outfile_name, "w")
    return outfile, None


def main(infile_name=None, outfile_name=None, in_place=False, divider=DIVIDER):
    with open_infile(infile_name) as infile:
        paragraphs = TaskItem.make_paragraphs(infile)
    out = make_tasks(paragraphs, divider)
    outfile, tmppath = open_outfile(outfile_name, in_place = in_place, infile_name = infile_name)
    try:
        display_tasks(out, outfile)
        if tmppath:
            outfile.flush() #or else we get a truncated file
            shutil.copy(tmppath, infile_name)
    finally:
        if outfile is not sys.stdout:
            outfile.close()
        if tmppath:
            os.remove(tmppath)
    if infile_name and outfile_name and outfile_name != infile_name:
        shutil.copystat(infile_name, outfile_name)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', default=None, help='Input file. Default is stdin')
    parser.add_argument('outfile', nargs='?', default=None, help='Output file. Default is stdout')
    parser.add_argument('-i', '--in-place', action="store_true", help="modify file in-place")
    parser.add_argument('-d', '--divider', default=DIVIDER)
    args = parser.parse_args()
    main(infile_name=args.infile, outfile_name=args.outfile, in_place=args.in_place, divider=args.divider)
