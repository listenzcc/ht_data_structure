# coding: utf-8

import os
import random
import datetime
import webbrowser

'''
This script is to parse directories in DS_dir.
'''

'''
# Function: find lastest DS_dir
# Output: DS_dir, directory of DS structure
'''
root_dir = 'C:\\Users\\liste\\Documents\\ht_data_structure'

DS_dirs = []
for d in os.listdir(root_dir):
    if os.path.isdir(os.path.join(root_dir, d)) and d.startswith('DS_'):
        print(d)
        DS_dirs.append(d)
DS_dirs.sort()

DS_dir = DS_dirs.pop()
print('-'*80)
print('DS: %s' % DS_dir)

'''
# Function: parse DS_dir
# Output: [html], build report in html
'''
names = dict()
name_list = []
tasks = dict()
task_list = []

dirs = os.listdir(DS_dir)

for d in dirs:
    s = d.split('_')
    name = s[-1]
    task = s[1]

    if name not in names.keys():
        names[name] = set()
        name_list.append(name)
    names[name].add(d)

    if task not in tasks.keys():
        tasks[task] = set()
        task_list.append(task)
    tasks[task].add(d)


def _get_date(e):
    # parse date information from dir name
    s = e.split('_')
    return s[3]


def _parse_date(e):
    # calculate datetime using 8-char string
    year = e[0:4]
    month = e[4:6]
    day = e[6:8]
    return datetime.datetime(int(year), int(month), int(day))


def parse_name(_name, fpath=None):

    report_in_html = False
    if fpath is not None:
        # if fpath is not none, read html tmp and open report html as f
        with open(os.path.join(root_dir, 'report_tmp.html'), 'r') as f:
            tmphtml = f.readlines()
        f = open(fpath, 'w')
        report_in_html = True

    def pnt_datas(_datas, _task=None):
        # print information for the subject
        # if _task is not none, print information only this task
        if report_in_html:
            if _task is None:
                _title = _name
            else:
                _title = '%s_%s' % (_name, _task)

            # write table head
            f.writelines([
                '<table>',
                '<caption>',
                '<h2 style="float: left">%s</h2>' % _title,
                '</caption>',
                '<thead>',
                '<tr>',
                '<th>Order</th>',
                '<th>Fname</th>',
                '<th>Delta</th>'
                '<th>Cum</th>',
                '</tr>',
                '</thead>',
                '<tbody>'])

        # sort _datas using date information
        _datas.sort(key=lambda e: _get_date(e))
        for i, e in enumerate(_datas):
            if i > 0:
                # calculate _delta if not first
                _first = _parse_date(_get_date(_datas[0]))
                _last = _parse_date(_get_date(_datas[i-1]))
                _this = _parse_date(_get_date(e))
                _delta = _this - _last
                _cum = _this - _first
                print('-passed: %d days' % _delta.days)
            print('%d: %s' % (i+1, e))

            # write table contents
            if report_in_html:
                f.write('<tr>')
                f.write('<td>%d</td>' % (i+1))
                f.write('<td>%s</td>' % e)
                if i > 0:
                    f.write('<td>%d days</td>' % _delta.days)
                    f.write('<td>%d days</td>' % _cum.days)
                else:
                    f.write('<td>---</td>')
                    f.write('<td>---</td>')
                f.write('</tr>')

        if report_in_html:
            # write table end
            f.writelines([
                '</tbody>',
                '</table>'])

        print('')

    if report_in_html:
        # write head until brief blocks
        while tmphtml:
            e = tmphtml.pop(0)
            f.write(e)
            if '<!--tobefilled: brief-->' in e:
                break

    print('-'*80)
    # working on subject for all tasks
    print('Working on %s:' % _name)
    _datas = [e for e in names[_name]]
    pnt_datas(_datas)

    print('For each task:')
    for _task in task_list:
        # working on subject for certain _task
        print('%s:' % _task)
        _datas = [e for e in names[_name] if e in tasks[_task]]
        pnt_datas(_datas, _task)

    if report_in_html:
        # write end and close html file
        while tmphtml:
            e = tmphtml.pop(0)
            f.write(e)
        f.close()


x = ''
while len(x) == 0:
    _name = random.choice(name_list)
    htmlpath = os.path.join(root_dir, 'a.html')
    parse_name(_name, htmlpath)
    webbrowser.open(htmlpath)
    x = input()

print('ends')
