# coding: utf-8

import os
import time
import random


'''
# Function: Init random variables for virtual DS building.
# Output: dates, random date list.
# Output: num_date, number of experiment dates.
# Output: names, random name list.
# Output: num_name, number of subject names.
# Output: tasks, random task list.
# Output: num_task, number of tasks.
'''

# date starts at (1976-01-01 00:00:00)
start = time.mktime((1976, 1, 1, 0, 0, 0, 0, 0, 0))
# date ends at (1990-12-31 23:59:59)
end = time.mktime((1990, 12, 31, 23, 59, 59, 0, 0, 0))


def rand_date(start=start, end=end, fmt='%Y%m%d'):
    # make random date from start to end
    t = random.randint(start, end)
    date_touple = time.localtime(t)
    return time.strftime(fmt, date_touple)


def rand_task():
    # make random task name, writtern as lower chars
    chrlst = [chr(i) for i in range(97, 97+26)]
    length = random.randint(5, 10)
    return ''.join(random.choices(chrlst, k=length))


def rand_name():
    # make random subject name, writtern as upper chars
    return rand_task().upper()


def list_norepeat(fun, n):
    # make list using fun as random element.
    # then shrink the list to no repeat element.
    lst = list(set(fun() for j in range(n)))
    return lst, len(lst)


def print_lst(lst):
    # print list
    # only print 10 elements if the list is too long
    print('-'*80)
    length = len(lst)
    print('Count: %d' % length)
    if length < 10:
        [print('%d: %s' % (i, e)) for i, e in enumerate(lst)]
    else:
        for i in range(5):
            print('%d: %s' % (i, lst[i]))
        print('...')
        for i in range(5):
            print('%d: %s' % (length-5+i, lst[length-5+i]))


# init numbers as good wish
# they are going to be replaced using list_norepeat
num_date = 1000
num_task = 5
num_name = 100

dates, num_date = list_norepeat(rand_date, num_date)
print_lst(dates)

tasks, num_task = list_norepeat(rand_task, num_task)
print_lst(tasks)

names, num_name = list_norepeat(rand_name, num_name)
print_lst(names)

'''
# Function: for each subject take in several experiment at random date
# Function: for each experiment, record it as a directory
# Output: [file], restore ground truth of experiment table
# Output: [DS], data structure in directory
'''

time_stamp = time.strftime('%Y%m%d-%H-%M-%S')
root_dir = 'C:\\Users\\liste\\Documents\\ht_data_structure'

ds_path = os.path.join(root_dir, 'DS_%s' % time_stamp)
gt_path = os.path.join(root_dir, 'GT_%s.recore' % time_stamp)

assert(not os.path.exists(ds_path))
assert(not os.path.exists(gt_path))

os.mkdir(ds_path)

with open(gt_path, 'w') as f:
    for s, _name in enumerate(names):
        # for each subject
        # it participants in several tasks
        _sub = 'Sub%03d' % (s+1)
        _num = random.randint(10, 20)
        _dates = random.sample(dates, k=_num)
        _dates.sort()
        _tasks = random.choices(tasks, k=_num)

        f.write('[Begin]: %s\n' % _name)

        for i in range(_num):
            _date = _dates[i]
            _task = _tasks[i]
            entry = '%s: (%d|%d) %s, %s\n' % (
                _name, i+1, _num, _date, _task)
            print(entry)
            f.write(entry)
            os.mkdir(os.path.join(ds_path, '%s_%s_%02d_%s_%s' %
                                  (_sub, _task, i+1, _date, _name)))

        f.write('[End]: %s\n' % _name)
