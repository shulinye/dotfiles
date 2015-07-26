#!/usr/bin/python3

DIVIDER = "Tasks Completed"

class TaskItem(object):
    """A class for tasks that's nestable."""
    def __init__(self, task, *tasks):
        self.task = task.rstrip()
        self.subtasks = set(TaskItem(i) for i in tasks if i != '')
    def join(self, other):
        if self.task != other.task: raise ValueError
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
        return "\n".join([self.task] + [str(i) for i in self.subtasks]) + '\n'
    def __repr__(self):
        return self.task.rstrip()
    def __lt__(self, other):
        return self.task < other.task
    def __eq__(self, other):
        return self.task == other.task
    def __hash__(self):
        return hash(self.task)

def makeparagraphs(intake):
    out = []
    for line in intake:
        if line.strip() == '': continue
        elif "\t" in line: out[-1] += line
        else: out.append(line)
    return (i for i in out)

def main(intake, divider = DIVIDER):
    tasks = set()
    done = set()
    f = []
    paragraphs = makeparagraphs(intake)

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
        if isinstance(i, TaskItem): print(i.display())
        else: print(i)

if __name__ == "__main__":
    import fileinput
    main(fileinput.input())
