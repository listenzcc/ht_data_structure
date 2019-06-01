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
    s = e.split('_')
    return s[3]


def _parse_date(e):
    year = e[0:4]
    month = e[4:6]
    day = e[6:8]
    return datetime.datetime(int(year), int(month), int(day))


def parse_name(_name, fpath=None):

    report_in_html = False
    if fpath is not None:
        with open(os.path.join(root_dir, 'report_tmp.html'), 'r') as f:
            tmphtml = f.readlines()
        f = open(fpath, 'w')
        report_in_html = True

    def pnt_datas(_datas, _task=None):
        _title = _name
        if _task is not None:
            _title += '_'
            _title += _task
        if report_in_html:
            f.writelines([
                '<table>',
                '<caption>',
                '<h2 style="float: left">%s</h2>' % _title,
                '</caption>',
                '<thead>',
                '<tr>',
                '<th>Order</th>',
                '<th>Fname</th>',
                '<th>Delta</th>',
                '</tr>',
                '</thead>',
                '<tbody>'])

        _datas.sort(key=lambda e: _get_date(e))
        for i, e in enumerate(_datas):
            if i > 0:
                _last = _parse_date(_get_date(_datas[i-1]))
                _this = _parse_date(_get_date(e))
                _delta = _this - _last
                print('-passed: %d days' % _delta.days)
            print('%d: %s' % (i+1, e))

            if report_in_html:
                f.write('<tr>')
                f.write('<td>%d</td>' % (i+1))
                f.write('<td>%s</td>' % e)
                if i > 0:
                    f.write('<td>%d days</td>' % _delta.days)
                else:
                    f.write('<td>---</td')
                f.write('</tr>')

        if report_in_html:
            f.writelines([
                '</tbody>',
                '</table>'])

        print('')

    print('-'*80)
    print('Working on %s:' % _name)
    _datas = [e for e in names[_name]]

    if report_in_html:
        while tmphtml:
            e = tmphtml.pop(0)
            f.write(e)
            if '<!--tobefilled: brief-->' in e:
                break
    pnt_datas(_datas)

    print('For each task:')
    for _task in task_list:
        print('%s:' % _task)
        _datas = [e for e in names[_name] if e in tasks[_task]]
        pnt_datas(_datas, _task)

    if report_in_html:
        while tmphtml:
            e = tmphtml.pop(0)
            f.write(e)
        f.close()


x = 's'
while x:
    _name = random.choice(name_list)
    htmlpath = os.path.join(root_dir, 'a.html')
    parse_name(_name, htmlpath)
    webbrowser.open(htmlpath)
    x = input()
