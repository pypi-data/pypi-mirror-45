# Copyright (C) 2019 Michał Góral.
#
# This file is part of TWC
#
# TWC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TWC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TWC. If not, see <http://www.gnu.org/licenses/>.

'''TaskWarrior utilities'''

import functools
from collections import OrderedDict, deque

from twc.task import Task


class TaskComparer:
    '''Class which can be used as a key in all Python sort methods for sorting
    TaskWarrior lists of task dictionaries. It compares tasks by applying a
    complex TaskWarrior-compatible sort conditions.'''
    def __init__(self, task, cmp):
        self.task = task
        self.cmp = cmp

    def __lt__(self, other):
        for attr, rev in self.cmp:
            sp = self.task.t[attr]
            op = other.task.t[attr]

            if sp is None and op is None:
                continue
            if sp is None:
                return True ^ rev
            if op is None:
                return False ^ rev
            if sp == op:
                continue
            return (sp < op) ^ rev

        # we're here because all checked attributes are equal
        return False


def _process_sort_string(sort_string):
    '''Returns a list of tuples: (sort condition, reverse sort)'''
    cmp = []
    for attr in sort_string.split(','):
        attr = attr.strip()
        rev = False

        if attr.endswith('+'):
            attr = attr[:-1]
        elif attr.endswith('-'):
            attr = attr[:-1]
            rev = True

        cmp.append((attr, rev))
    return cmp


def execute_command(args, tw):
    stdout, stderr, retcode = tw.execute_command(
        args,
        return_all=True,
        allow_failure=False)
    return stdout, stderr, (retcode == 0)


def filter_tasks(filter_string, tw):
    '''Returns a list of tasks filtered by a given TW-compatible string'''
    if filter_string:
        tasks = tw.tasks.filter(filter_string)
    else:
        tasks = tw.tasks.all()

    return [Task(t) for t in tasks]


def sort_tasks(tasks, sort_string):
    '''Sorts a list of tasks (in-place) according to a complex TW-compatible
    sort string.'''
    if not sort_string:
        return

    cmp = _process_sort_string(sort_string)
    comparer = functools.partial(TaskComparer, cmp=cmp)
    tasks.sort(key=comparer)


def group_tasks(tasks):
    '''Groups tasks by creating parent-child relationship. This allows creating subtasks
    even if TaskWarrior doesn't natively supports that.

    Tasks are grouped by their `depends` field: parent tasks depend on
    children.'''
    grouped = OrderedDict([(task['uuid'], task) for task in tasks])
    for task in tasks:
        deps = task.t['depends']
        for dep_task in deps:
            dep_uuid = dep_task['uuid']
            dep = grouped.get(dep_uuid)
            if dep:
                task.add_child(dep)
                del grouped[dep_uuid]

    return grouped


def dfs(tasks):
    '''Depth-first-search walk through tasks grouped by group_tasks()'''
    stack = deque(tasks)
    while stack:
        task = stack.popleft()
        yield task
        stack.extendleft(task.children)
