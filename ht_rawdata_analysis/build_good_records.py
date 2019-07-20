#!/usr/bin/env python
# coding: utf-8

import os
import sys
import json


class ExperimentRecord():
    """
    Experiment record, a class for parse experiment information from target path
    """

    def __init__(self, path):
        # Init, parse and print information
        self.path = path
        self._parse_dir()
        self._print()

    def _parse_dir(self):
        # parse file information
        base_name = os.path.basename(self.path)
        date, session = base_name.split('_')

        # Open inf file for subject information
        # name: name of the subject + task information
        # age: age of the subject
        with open(os.path.join(self.path, 'NIRS-%s.inf' % base_name)) as f:
            lines = f.readlines()
            name = lines[1].split('=')[1].replace('"', '').strip()
            age = lines[2].split('=')[1].strip()

        # If name is too short, throw IndexError
        if len(name) < 3:
            raise IndexError

        # Recording informations
        self.info = dict(path=self.path,
                         date=date,
                         session=session,
                         name=name,
                         age=age,)

    def _print(self, f=sys.stdout):
        # Print information
        print('', file=f)
        [print('%s: %s' % (e[0], e[1]), file=f) for e in self.info.items()]
        print('', file=f)

    def _record(self, f):
        # Print information into file as f
        self._print(f)


def folder_check(path, depth, max_depth=5):
    # Warning: this is a iterable function
    # Check if path is good path
    # path: current path
    # depth: current depth from root
    # max_depth: we do not search if it is too deep

    # Parse path
    base_name = os.path.basename(path)
    par_name = os.path.basename(os.path.dirname(path))

    # base_name contains par_name infers we may have found sessions from one day
    # only if base_name follows some rules: date + session
    # and NIRS-balabala.inf should in the path
    if all([base_name.startswith(par_name),
            len(base_name.split('_')) == 2,
            len(base_name.split('-')) == 3,
            'NIRS-%s.inf' % base_name in os.listdir(path)]):
        # print('good:', path)
        try:
            # Parse the path and record the information
            good_records.append(ExperimentRecord(path))
        except IndexError:
            # If it fails, the path is to be checked
            bad_path.append(path)
        return

    # Stop iteration if max_depth is reached
    if depth == max_depth:
        return

    # Go in deeper
    [folder_check(os.path.join(path, p), depth+1)
     for p in os.listdir(path) if os.path.isdir(os.path.join(path, p))]


#####################################################################
# We do not want to save files anywhere
workingdir = 'C:\\Users\\zcc\\Documents\\ht_rawdata_analysis'
resultdir = os.path.join(workingdir, 'results')
if not os.path.exists(resultdir):
    os.mkdir(resultdir)


#####################################################################
# Where we start searching
root = 'D:\\DataBackUp\\UnArchivedData\\Temporary\\CurrentStudents_Start-20190505\\wukun'

# Init variables for recording
# good_records: the experiment sessions we can correctly read
# bad_path: the path seems to be experiment fold, however some information is wrong
good_records = []
bad_path = []

# Searching starts
folder_check(root, 0)


#####################################################################
# Write good_records as json for useable
with open(os.path.join(resultdir, 'good_records.json'), 'w') as f:
    json.dump([e.info for e in good_records], f)

# Write bad_path as txt for quick readable
with open(os.path.join(resultdir, 'bad_path.txt'), 'w') as f:
    f.writelines(bad_path)
