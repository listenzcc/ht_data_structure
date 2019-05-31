# coding: utf-8

import os
import time
import random

# date starts at (1976-01-01 00:00:00)
start = time.mktime((1976, 1, 1, 0, 0, 0, 0, 0, 0))
# date ends at (1990-12-31 23:59:59)
end = time.mktime((1990, 12, 31, 23, 59, 59, 0, 0, 0))


def rand_date(start=start, end=end, fmt='%Y%m%d'):
    t = random.randint(start, end)
    date_touple = time.localtime(t)
    return time.strftime(fmt, date_touple)


def rand_task():
    chrlst = [chr(i) for i in range(97, 97+26)]
    length = random.randint(5, 10)
    return ''.join(random.choices(chrlst, k=length))


def rand_name():
    return rand_task().upper()


def list_nonrepeat(fun, n):
    lst = list(set(fun() for j in range(n)))
    return lst, len(lst)


def print_lst(lst):
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


num_date = 1000
num_task = 3
num_name = 100

dates, num_date = list_nonrepeat(rand_date, num_date)
print_lst(dates)

tasks, num_task = list_nonrepeat(rand_task, num_task)
print_lst(tasks)

names, num_name = list_nonrepeat(rand_name, num_name)
print_lst(names)
