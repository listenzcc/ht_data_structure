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
num_task = 3
num_name = 100

dates, num_date = list_norepeat(rand_date, num_date)
print_lst(dates)

tasks, num_task = list_norepeat(rand_task, num_task)
print_lst(tasks)

names, num_name = list_norepeat(rand_name, num_name)
print_lst(names)

'''
# Function: for each subject take in several experiment at random date
# Output: no output.
'''
