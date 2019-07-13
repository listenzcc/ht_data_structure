#!/usr/bin/env python
# coding: utf-8

import time
import os


class DataDir():
    def __init__(self, _dir, _root):
        self._dir = _dir
        if not self._legal():
            return

        self._root = _root
        ds = _dir.split('_')
        self._idx = int(ds[0])
        self._name = ds[1]

        self._parse_subdir()

    def _legal(self, _dir=None):
        return all([self._dir[0] in [str(i) for i in range(1, 10)],
                    len(self._dir.split('_')) == 2])

    def _parse_subdir(self):
        curdir = os.path.join(self._root, self._dir)
        subdirs = os.listdir(curdir)
        for i, e in enumerate(subdirs):
            isgood = True
            es = e.split('_')
            if not len(es) == 5:
                isgood = False
            else:
                if all([es[0] == 'sub%03d' % self._idx,
                        es[1] in ['aud', 'rest'],
                        es[2] in ['NIRS'],
                        len(es[3]) == 8]):
                    pass
                else:
                    isgood = False

            if isgood:
                subdirs[i] = '[Checked]  ' + e
                continue

            guess = self._hardguess(e)
            if guess:
                subdirs[i] = '[Rename]   ' + e + ' -> sub%03d_%s_%s_%s_%s' % (
                    self._idx,
                    guess['task'],
                    guess['img'],
                    guess['date'],
                    self._name)
            else:
                subdirs[i] = '[Leave]    ' + e

        self._subdirs = subdirs

    def _hardguess(self, _expdir):
        if len(_expdir) < 20:
            return False

        guess = {}
        if self._name in _expdir:
            guess['name'] = self._name
        else:
            return False

        for _task in ['aud', 'rest']:
            for _img in ['NIRS']:
                if _task+_img in _expdir:
                    guess['task'] = _task
                    guess['img'] = _img
                    break

        if 'task' not in guess.keys():
            return False

        _date = _expdir[-14:-4]
        if _date[4] == '-' and _date[7] == '-':
            newdate = ''.join(_date.split('-'))
            if not len(newdate) == 8:
                return False
        else:
            return False

        guess['date'] = newdate

        return guess

    def _pnt(self):
        print('-' * 80)
        pre = ' ' * 8
        print('%03d:' % self._idx, self._dir)
        print(pre, pre, self._root)
        [print(pre, e) for e in self._subdirs]

    def _rename_subdir(self):
        self._pnt()
        for sd in self._subdirs:
            if sd.startswith('[Rename]'):
                sdsp = sd.split()
                print('Rename: from %s to %s' % (sdsp[1], sdsp[3]))
                os.rename(os.path.join(self._root, self._dir, sdsp[1]),
                          os.path.join(self._root, self._dir, sdsp[3]))


root = os.path.join(
    'D:\\DataBackUp\\UnArchivedData\\Temporary\\rawdata_0709')

subject_dirs = sorted([DataDir(d, root)
                       for d in os.listdir(root) if DataDir(d, root)._legal()],
                      key=lambda e: e._idx)

# for dd in subject_dirs:
#     dd._pnt()

for dd in subject_dirs:
    dd._rename_subdir()
